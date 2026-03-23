/**
 * Static markdown reader for GitHub Pages.
 * Query: ?page=content/phase-1/week-1/day-1.md
 */
(function () {
  "use strict";

  const DEFAULT_PAGE = "content/syllabus.md";
  const INDEX_DIR = window.location.href.replace(/[^/]*$/, "");

  const articleEl = document.getElementById("article");
  const titleEl = document.getElementById("doc-title");
  const breadcrumbEl = document.getElementById("breadcrumb");
  const tocEl = document.getElementById("toc");
  const bentoGridEl = document.querySelector(".bento-grid");
  const sidebarLinksMountEl = document.getElementById("sidebar-links-mount");
  const sidebarLinksCardEl = document.getElementById("sidebar-links-card");
  const sidebarChecklistMountEl = document.getElementById("sidebar-checklist-mount");
  const sidebarChecklistCardEl = document.getElementById("sidebar-checklist-card");
  const sidebarChecklistRailEl = document.getElementById("sidebar-checklist-rail");
  const browseEl = document.getElementById("browse");
  const fabNavEl = document.getElementById("fab-nav");
  const statusEl = document.getElementById("status");
  const fab = document.getElementById("fab");
  const fabPanel = document.getElementById("fab-panel");
  const fabClose = document.getElementById("fab-close");
  const themeToggle = document.getElementById("theme-toggle");
  const searchWrap = document.getElementById("site-search");
  const searchInput = document.getElementById("site-search-input");
  const searchPanel = document.getElementById("site-search-panel");
  const searchListbox = document.getElementById("site-search-listbox");

  const THEME_STORAGE_KEY = "applied-ai-theme";
  const CHECKLIST_STORAGE_PREFIX = "applied-ai-checklist:";

  let manifestPages = [];
  let searchIndex = [];
  let lastSearchPaths = [];
  let searchActiveIdx = -1;
  let currentPagePath = DEFAULT_PAGE;
  /** Monotonic counter so only the latest loadPage() may mutate the DOM (avoids stale fetch races). */
  let loadPageSeq = 0;
  /** Remove scroll/resize listeners from the previous TOC scroll-spy (if any). */
  let tocSpyCleanup = null;

  const FETCH_DOC = { cache: "no-store" };

  if (typeof marked !== "undefined") {
    marked.setOptions({ gfm: true, breaks: false });
  }

  function getQueryPage() {
    const params = new URLSearchParams(window.location.search);
    const p = params.get("page");
    return p ? decodeURIComponent(p.trim()) : null;
  }

  function isAllowedPath(p) {
    if (!p || typeof p !== "string") return false;
    const n = p.replace(/\\/g, "/");
    if (n.includes("..") || n.includes("//")) return false;
    if (!n.startsWith("content/")) return false;
    if (!n.endsWith(".md")) return false;
    return true;
  }

  /** Static assessment JSON under assessments/ (GitHub Pages). */
  function isAllowedAssessmentPath(p) {
    if (!p || typeof p !== "string") return false;
    const n = p.replace(/\\/g, "/").trim();
    if (n.includes("..") || n.includes("//")) return false;
    if (!n.startsWith("assessments/")) return false;
    if (!n.endsWith(".json")) return false;
    return true;
  }

  /** Slide deck JSON under content/…/slides/ (GitHub Pages). */
  function isAllowedSlidesPath(p) {
    if (!p || typeof p !== "string") return false;
    const n = p.replace(/\\/g, "/").trim();
    if (n.includes("..") || n.includes("//")) return false;
    if (!n.startsWith("content/")) return false;
    if (!n.includes("/slides/")) return false;
    if (!n.endsWith(".json")) return false;
    return true;
  }

  function escapeAttr(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;");
  }

  /** Parse a leading "..." string with \\n, \\t, \\", \\\\ escapes; trailing text after closing " is invalid. */
  function parseDoubleQuotedString(s) {
    const t = String(s).trim();
    if (!t.startsWith('"')) return null;
    let i = 1;
    let out = "";
    while (i < t.length) {
      const c = t[i];
      if (c === "\\") {
        if (i + 1 >= t.length) return null;
        const n = t[++i];
        if (n === "n") out += "\n";
        else if (n === "r") out += "\r";
        else if (n === "t") out += "\t";
        else if (n === '"' || n === "\\") out += n;
        else out += n;
        i++;
        continue;
      }
      if (c === '"') {
        if (t.slice(i + 1).trim() !== "") return null;
        return out;
      }
      out += c;
      i++;
    }
    return null;
  }

  /**
   * <% component_name args %>
   * Example: <% quiz assessments/phase-1/week-1/green-brown.json %>
   * Slides: <% slides content/phase-1/week-1/slides/day-1.json %>
   */
  const MD_COMPONENT_RE = /<%\s*(\w+)\s+([\s\S]*?)\s*%>/g;

  function preprocessMarkdownComponents(md) {
    return md.replace(MD_COMPONENT_RE, function (_full, name, args) {
      const trimmed = String(args || "").trim();
      if (name === "quiz") {
        if (!trimmed || !isAllowedAssessmentPath(trimmed)) {
          return '<p class="prose prose--error">Invalid or missing quiz path.</p>';
        }
        return (
          '<div class="md-component md-component--quiz" data-md-component="quiz" data-json="' +
          escapeAttr(trimmed) +
          '"></div>'
        );
      }
      if (name === "checklist") {
        const lines = String(trimmed)
          .split(/\r?\n/)
          .map(function (l) {
            return l.trim();
          })
          .filter(Boolean);
        if (!lines.length) {
          return '<p class="prose prose--error">Checklist is empty.</p>';
        }
        return (
          '<div class="md-component md-component--checklist" data-md-component="checklist" data-items="' +
          escapeAttr(JSON.stringify(lines)) +
          '"></div>'
        );
      }
      if (name === "links") {
        const lines = String(trimmed)
          .split(/\r?\n/)
          .map(function (l) {
            return l.trim();
          })
          .filter(Boolean);
        const headingRe = /^(#{1,6})\s+(.+)$/;
        const linkLineRe = /\[([^\]]*)\]\(([^)]+)\)/g;
        const groups = [];
        let current = { heading: null, items: [] };

        function flush() {
          if (current.items.length > 0) {
            groups.push({
              heading: current.heading,
              items: current.items.slice(),
            });
          }
          current = { heading: null, items: [] };
        }

        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          const hm = headingRe.exec(line);
          if (hm) {
            flush();
            current.heading = hm[2].trim();
            continue;
          }
          let m;
          linkLineRe.lastIndex = 0;
          while ((m = linkLineRe.exec(line)) !== null) {
            current.items.push({ label: m[1].trim(), href: m[2].trim() });
          }
        }
        flush();

        const totalItems = groups.reduce(function (sum, g) {
          return sum + g.items.length;
        }, 0);
        if (!totalItems) {
          return '<p class="prose prose--error">Links component is empty.</p>';
        }
        return (
          '<div class="md-component md-component--links" data-md-component="links" data-items="' +
          escapeAttr(JSON.stringify({ groups: groups })) +
          '"></div>'
        );
      }
      if (name === "slides") {
        if (!trimmed || !isAllowedSlidesPath(trimmed)) {
          return '<p class="prose prose--error">Invalid or missing slides path.</p>';
        }
        return (
          '<div class="md-component md-component--slides" data-md-component="slides" data-json="' +
          escapeAttr(trimmed) +
          '"></div>'
        );
      }
      if (name === "editor") {
        const tokens = String(trimmed)
          .split(/\s+/)
          .map(function (t) {
            return t.trim();
          })
          .filter(Boolean);
        if (tokens.length < 1) {
          return '<p class="prose prose--error">Invalid editor: need a variant.</p>';
        }
        const variant = tokens[0];
        if (variant === "markdown") {
          const afterVariant = String(trimmed).replace(/^\s*markdown\s+/, "");
          const defaultText = parseDoubleQuotedString(afterVariant.trim());
          if (defaultText === null) {
            return (
              '<p class="prose prose--error">Invalid editor: markdown needs a quoted default string (e.g. ' +
              '<code>&lt;% editor markdown &quot;# Line\\n&quot; %&gt;</code>).</p>'
            );
          }
          return (
            '<div class="md-component md-component--editor" data-md-component="editor" data-variant="' +
            escapeAttr(variant) +
            '" data-initial-markdown="' +
            escapeAttr(JSON.stringify(defaultText)) +
            '"></div>'
          );
        }
        if (tokens.length < 2) {
          return '<p class="prose prose--error">Invalid editor: need a variant and a JSON path.</p>';
        }
        const jsonPath = tokens.slice(1).join(" ");
        if (!isAllowedAssessmentPath(jsonPath)) {
          return '<p class="prose prose--error">Invalid or missing editor JSON path.</p>';
        }
        return (
          '<div class="md-component md-component--editor" data-md-component="editor" data-variant="' +
          escapeAttr(variant) +
          '" data-json="' +
          escapeAttr(jsonPath) +
          '"></div>'
        );
      }
      return (
        '<p class="prose prose--error">Unknown component: ' +
        escapeHtml(name) +
        "</p>"
      );
    });
  }

  let quizScriptPromise = null;
  let editorScriptPromise = null;
  let slidesScriptPromise = null;

  function ensureQuizCss() {
    if (document.querySelector("link[data-applied-ai-quiz-css]")) {
      return Promise.resolve();
    }
    return new Promise(function (resolve) {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = new URL("styles/quiz.css", INDEX_DIR).href;
      link.setAttribute("data-applied-ai-quiz-css", "");
      link.onload = function () {
        resolve();
      };
      link.onerror = function () {
        resolve();
      };
      document.head.appendChild(link);
    });
  }

  function ensureQuizScript() {
    if (typeof window.AppliedAIQuiz !== "undefined" && window.AppliedAIQuiz.mount) {
      return Promise.resolve();
    }
    if (!quizScriptPromise) {
      quizScriptPromise = new Promise(function (resolve, reject) {
        const s = document.createElement("script");
        s.src = new URL("js/quiz.js", INDEX_DIR).href;
        s.async = true;
        s.onload = function () {
          resolve();
        };
        s.onerror = function () {
          quizScriptPromise = null;
          reject(new Error("Failed to load quiz.js"));
        };
        document.head.appendChild(s);
      });
    }
    return quizScriptPromise;
  }

  function ensureEditorCss() {
    if (document.querySelector("link[data-applied-ai-editor-css]")) {
      return Promise.resolve();
    }
    return new Promise(function (resolve) {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = new URL("styles/editor.css", INDEX_DIR).href;
      link.setAttribute("data-applied-ai-editor-css", "");
      link.onload = function () {
        resolve();
      };
      link.onerror = function () {
        resolve();
      };
      document.head.appendChild(link);
    });
  }

  function ensureEditorScript() {
    if (typeof window.AppliedAIEditor !== "undefined" && window.AppliedAIEditor.mount) {
      return Promise.resolve();
    }
    if (!editorScriptPromise) {
      editorScriptPromise = new Promise(function (resolve, reject) {
        const s = document.createElement("script");
        s.src = new URL("js/editor.js", INDEX_DIR).href;
        s.async = true;
        s.onload = function () {
          resolve();
        };
        s.onerror = function () {
          editorScriptPromise = null;
          reject(new Error("Failed to load editor.js"));
        };
        document.head.appendChild(s);
      });
    }
    return editorScriptPromise;
  }

  function ensureSlidesCss() {
    if (document.querySelector("link[data-applied-ai-slides-css]")) {
      return Promise.resolve();
    }
    return new Promise(function (resolve) {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = new URL("styles/slides.css", INDEX_DIR).href;
      link.setAttribute("data-applied-ai-slides-css", "");
      link.onload = function () {
        resolve();
      };
      link.onerror = function () {
        resolve();
      };
      document.head.appendChild(link);
    });
  }

  function ensureSlidesScript() {
    if (typeof window.AppliedAISlides !== "undefined" && window.AppliedAISlides.mount) {
      return Promise.resolve();
    }
    if (!slidesScriptPromise) {
      slidesScriptPromise = new Promise(function (resolve, reject) {
        const s = document.createElement("script");
        s.src = new URL("js/slides.js", INDEX_DIR).href;
        s.async = true;
        s.onload = function () {
          resolve();
        };
        s.onerror = function () {
          slidesScriptPromise = null;
          reject(new Error("Failed to load slides.js"));
        };
        document.head.appendChild(s);
      });
    }
    return slidesScriptPromise;
  }

  function readChecklistState(pagePath) {
    try {
      const raw = localStorage.getItem(CHECKLIST_STORAGE_PREFIX + pagePath);
      if (!raw) return null;
      const data = JSON.parse(raw);
      return Array.isArray(data) ? data : null;
    } catch {
      return null;
    }
  }

  function writeChecklistState(pagePath, state) {
    try {
      localStorage.setItem(CHECKLIST_STORAGE_PREFIX + pagePath, JSON.stringify(state));
    } catch {
      /* ignore */
    }
  }

  function ensureChecklistRows(state, listIndex, len) {
    while (state.length <= listIndex) state.push([]);
    const row = state[listIndex];
    while (row.length < len) row.push(false);
    row.length = len;
  }

  function renderChecklistLabelHtml(text) {
    if (typeof marked !== "undefined" && typeof marked.parseInline === "function") {
      return marked.parseInline(text);
    }
    return escapeHtml(text);
  }

  function hydrateChecklists(root, seq) {
    const nodes = root.querySelectorAll('[data-md-component="checklist"]');
    if (!nodes.length) return;

    let state = readChecklistState(currentPagePath);
    if (!state) state = [];

    nodes.forEach(function (el, listIndex) {
      if (seq !== loadPageSeq) return;
      let items;
      try {
        items = JSON.parse(el.getAttribute("data-items") || "[]");
      } catch {
        el.innerHTML = '<p class="prose prose--error">Invalid checklist.</p>';
        return;
      }
      if (!Array.isArray(items) || !items.length) {
        el.innerHTML = '<p class="prose prose--error">Checklist is empty.</p>';
        return;
      }

      ensureChecklistRows(state, listIndex, items.length);

      const ul = document.createElement("ul");
      ul.className = "interactive-checklist";
      ul.setAttribute("role", "list");

      items.forEach(function (text, itemIndex) {
        const checked = !!state[listIndex][itemIndex];
        const inputId = "checklist-" + listIndex + "-" + itemIndex;

        const li = document.createElement("li");
        li.className = "interactive-checklist__item";

        const input = document.createElement("input");
        input.type = "checkbox";
        input.className = "interactive-checklist__checkbox";
        input.id = inputId;
        input.checked = checked;

        const label = document.createElement("label");
        label.className = "interactive-checklist__label";
        label.htmlFor = inputId;
        const span = document.createElement("span");
        span.className = "interactive-checklist__text";
        span.innerHTML = renderChecklistLabelHtml(String(text));

        label.appendChild(input);
        label.appendChild(span);
        li.appendChild(label);
        ul.appendChild(li);

        input.addEventListener("change", function () {
          if (seq !== loadPageSeq) return;
          state[listIndex][itemIndex] = input.checked;
          writeChecklistState(currentPagePath, state);
        });
      });

      el.innerHTML = "";
      el.removeAttribute("data-items");
      el.appendChild(ul);
    });
  }

  function updateSidebarRailVisibility() {
    const hasLinks = !!(sidebarLinksMountEl && sidebarLinksMountEl.children.length);
    const hasChecklist = !!(sidebarChecklistMountEl && sidebarChecklistMountEl.children.length);
    if (sidebarLinksCardEl) sidebarLinksCardEl.hidden = !hasLinks;
    if (sidebarChecklistCardEl) sidebarChecklistCardEl.hidden = !hasChecklist;
    const show = hasLinks || hasChecklist;
    if (sidebarChecklistRailEl) sidebarChecklistRailEl.hidden = !show;
    if (bentoGridEl) bentoGridEl.classList.toggle("has-sidebar-checklist", !!show);
  }

  function clearSidebarRail() {
    if (sidebarLinksMountEl) sidebarLinksMountEl.innerHTML = "";
    if (sidebarChecklistMountEl) sidebarChecklistMountEl.innerHTML = "";
    if (sidebarLinksCardEl) sidebarLinksCardEl.hidden = true;
    if (sidebarChecklistCardEl) sidebarChecklistCardEl.hidden = true;
    if (sidebarChecklistRailEl) sidebarChecklistRailEl.hidden = true;
    if (bentoGridEl) bentoGridEl.classList.remove("has-sidebar-checklist");
  }

  function hydrateLinks(root, seq) {
    const nodes = root.querySelectorAll('[data-md-component="links"]');
    if (!nodes.length) return;

    nodes.forEach(function (el) {
      if (seq !== loadPageSeq) return;
      let parsed;
      try {
        parsed = JSON.parse(el.getAttribute("data-items") || "{}");
      } catch {
        el.innerHTML = '<p class="prose prose--error">Invalid links.</p>';
        return;
      }
      let groups;
      if (parsed && Array.isArray(parsed.groups)) {
        groups = parsed.groups;
      } else if (Array.isArray(parsed)) {
        groups = [{ heading: null, items: parsed }];
      } else {
        el.innerHTML = '<p class="prose prose--error">Invalid links.</p>';
        return;
      }
      const totalItems = groups.reduce(function (sum, g) {
        return sum + (g.items && g.items.length ? g.items.length : 0);
      }, 0);
      if (!totalItems) {
        el.innerHTML = '<p class="prose prose--error">Links are empty.</p>';
        return;
      }

      const stack = document.createElement("div");
      stack.className = "sidebar-links-stack";

      groups.forEach(function (group) {
        const items = group.items || [];
        if (!items.length) return;
        const heading = group.heading != null && String(group.heading).trim() !== "" ? String(group.heading).trim() : null;

        const section = document.createElement("div");
        section.className = "sidebar-links-group";

        if (heading) {
          const h = document.createElement("h3");
          h.className = "sidebar-links__subheading";
          h.textContent = heading;
          section.appendChild(h);
        }

        const ul = document.createElement("ul");
        ul.className = "sidebar-links";
        ul.setAttribute("role", "list");

        items.forEach(function (item) {
          const li = document.createElement("li");
          li.className = "sidebar-links__item";
          const a = document.createElement("a");
          a.className = "sidebar-links__link";
          a.href = String(item.href || "#");
          a.innerHTML = renderChecklistLabelHtml(String(item.label || item.href || ""));
          li.appendChild(a);
          ul.appendChild(li);
        });

        section.appendChild(ul);
        stack.appendChild(section);
      });

      el.innerHTML = "";
      el.removeAttribute("data-items");
      el.appendChild(stack);
    });
  }

  /**
   * Moves link lists from the article into the right-hand rail (above the checklist).
   * Strips a leading “Links” heading and optional hr so the main column does not show gaps.
   */
  function moveLinksToSidebar(articleRoot, seq) {
    if (!sidebarLinksMountEl) return;

    const nodes = articleRoot.querySelectorAll(".md-component--links");
    if (!nodes.length) return;

    nodes.forEach(function (el) {
      if (seq !== loadPageSeq) return;
      let prev = el.previousElementSibling;
      if (prev && prev.tagName === "H2" && /^links$/i.test((prev.textContent || "").trim())) {
        prev.remove();
      }
      prev = el.previousElementSibling;
      if (prev && prev.tagName === "HR") {
        prev.remove();
      }
      sidebarLinksMountEl.appendChild(el);
    });
  }

  /**
   * Moves interactive checklists from the article into the right-hand checklist rail.
   * Strips a leading “Checklist” heading and optional hr so the main column does not show gaps.
   */
  function moveChecklistsToSidebar(articleRoot, seq) {
    if (!sidebarChecklistMountEl) return;

    const nodes = articleRoot.querySelectorAll(".md-component--checklist");
    if (!nodes.length) return;

    nodes.forEach(function (el) {
      if (seq !== loadPageSeq) return;
      let prev = el.previousElementSibling;
      if (prev && prev.tagName === "H2" && /^checklist$/i.test((prev.textContent || "").trim())) {
        prev.remove();
      }
      prev = el.previousElementSibling;
      if (prev && prev.tagName === "HR") {
        prev.remove();
      }
      sidebarChecklistMountEl.appendChild(el);
    });
  }

  async function hydrateMarkdownComponents(root, seq) {
    const quizNodes = root.querySelectorAll('[data-md-component="quiz"]');
    const editorNodes = root.querySelectorAll('[data-md-component="editor"]');
    const slideNodes = root.querySelectorAll('[data-md-component="slides"]');
    if (!quizNodes.length && !editorNodes.length && !slideNodes.length) return;

    let quizOk = true;
    let editorOk = true;
    let slidesOk = true;
    if (quizNodes.length) {
      try {
        await Promise.all([ensureQuizCss(), ensureQuizScript()]);
      } catch {
        quizOk = false;
      }
    }
    if (editorNodes.length) {
      try {
        await Promise.all([ensureEditorCss(), ensureEditorScript()]);
      } catch {
        editorOk = false;
      }
    }
    if (slideNodes.length) {
      try {
        await Promise.all([ensureSlidesCss(), ensureSlidesScript()]);
      } catch {
        slidesOk = false;
      }
    }
    if (seq !== loadPageSeq) return;

    if (!quizOk) {
      quizNodes.forEach(function (el) {
        el.innerHTML = '<p class="prose prose--error">Quiz module failed to load.</p>';
      });
    } else if (window.AppliedAIQuiz && window.AppliedAIQuiz.mount) {
      quizNodes.forEach(function (el) {
        if (seq !== loadPageSeq) return;
        const jsonPath = el.getAttribute("data-json");
        if (!jsonPath || !isAllowedAssessmentPath(jsonPath)) {
          el.innerHTML = '<p class="prose prose--error">Invalid quiz path.</p>';
          return;
        }
        window.AppliedAIQuiz.mount(el, jsonPath, INDEX_DIR);
      });
    }

    if (!editorOk) {
      editorNodes.forEach(function (el) {
        el.innerHTML = '<p class="prose prose--error">Editor module failed to load.</p>';
      });
    } else if (window.AppliedAIEditor && window.AppliedAIEditor.mount) {
      editorNodes.forEach(function (el) {
        if (seq !== loadPageSeq) return;
        const jsonPath = el.getAttribute("data-json");
        const variant = el.getAttribute("data-variant") || "";
        if (variant === "markdown") {
          window.AppliedAIEditor.mount(el, null, INDEX_DIR, variant);
          return;
        }
        if (!jsonPath || !isAllowedAssessmentPath(jsonPath)) {
          el.innerHTML = '<p class="prose prose--error">Invalid editor path.</p>';
          return;
        }
        window.AppliedAIEditor.mount(el, jsonPath, INDEX_DIR, variant);
      });
    }

    if (!slidesOk) {
      slideNodes.forEach(function (el) {
        el.innerHTML = '<p class="prose prose--error">Slides module failed to load.</p>';
      });
    } else if (window.AppliedAISlides && window.AppliedAISlides.mount) {
      slideNodes.forEach(function (el) {
        if (seq !== loadPageSeq) return;
        const jsonPath = el.getAttribute("data-json");
        if (!jsonPath || !isAllowedSlidesPath(jsonPath)) {
          el.innerHTML = '<p class="prose prose--error">Invalid slides path.</p>';
          return;
        }
        window.AppliedAISlides.mount(el, jsonPath, INDEX_DIR);
      });
    }
  }

  function pageUrl(pagePath) {
    const u = new URL(window.location.pathname, window.location.origin);
    u.searchParams.set("page", pagePath);
    return u.pathname + u.search + u.hash;
  }

  function getTheme() {
    return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }

  function syncThemeToggle() {
    if (!themeToggle) return;
    const dark = getTheme() === "dark";
    themeToggle.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    themeToggle.setAttribute("title", dark ? "Light mode" : "Dark mode");
  }

  function applyTheme(theme) {
    if (theme === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    syncThemeToggle();
  }

  function initThemeToggle() {
    if (!themeToggle) return;
    syncThemeToggle();
    themeToggle.addEventListener("click", function () {
      const next = getTheme() === "dark" ? "light" : "dark";
      applyTheme(next);
      try {
        localStorage.setItem(THEME_STORAGE_KEY, next);
      } catch {
        /* ignore */
      }
    });
  }

  function showStatus(msg, ms) {
    if (!statusEl) return;
    statusEl.textContent = msg;
    statusEl.classList.add("is-visible");
    clearTimeout(showStatus._t);
    showStatus._t = setTimeout(function () {
      statusEl.classList.remove("is-visible");
    }, ms || 3200);
  }

  function slugify(text) {
    return text
      .toLowerCase()
      .replace(/[^\w\s-]/g, "")
      .trim()
      .replace(/\s+/g, "-");
  }

  function dirnameOfFileUrl(filePath) {
    const fileUrl = new URL(filePath, INDEX_DIR);
    const s = fileUrl.href;
    return s.replace(/[^/]+$/, "");
  }

  function pathToContentKey(pathname) {
    const idx = pathname.indexOf("/content/");
    if (idx === -1) return null;
    let rel = pathname.slice(idx + 1);
    rel = rel.split("?")[0];
    if (!rel.endsWith(".md") || rel.includes("..")) return null;
    return rel;
  }

  function resolveMdHref(href, fromMdPath) {
    if (!href || href.startsWith("mailto:") || href.startsWith("#")) return null;
    if (/^https?:\/\//i.test(href)) {
      try {
        const u = new URL(href);
        if (u.origin !== window.location.origin) return null;
        return pathToContentKey(u.pathname);
      } catch {
        return null;
      }
    }
    const baseDir = dirnameOfFileUrl(fromMdPath);
    let resolved;
    try {
      resolved = new URL(href, baseDir);
    } catch {
      return null;
    }
    return pathToContentKey(resolved.pathname);
  }

  /**
   * External (other origin) → new tab. Same-origin, #fragment, mailto, tel → current tab.
   */
  function applyArticleLinkTargets(root) {
    root.querySelectorAll("a[href]").forEach(function (a) {
      const href = a.getAttribute("href");
      if (!href) return;
      if (href.startsWith("#")) {
        a.removeAttribute("target");
        a.removeAttribute("rel");
        return;
      }
      if (/^mailto:/i.test(href) || /^tel:/i.test(href)) {
        a.removeAttribute("target");
        a.removeAttribute("rel");
        return;
      }
      if (/^javascript:/i.test(href)) return;
      let u;
      try {
        if (href.startsWith("/")) {
          u = new URL(href, window.location.origin);
        } else if (/^https?:\/\//i.test(href)) {
          u = new URL(href);
        } else {
          u = new URL(href, dirnameOfFileUrl(currentPagePath));
        }
      } catch {
        return;
      }
      if (u.origin !== window.location.origin) {
        a.setAttribute("target", "_blank");
        a.setAttribute("rel", "noopener noreferrer");
      } else {
        a.removeAttribute("target");
        a.removeAttribute("rel");
      }
    });
  }

  function buildToc(container) {
    tocEl.innerHTML = "";
    const headings = container.querySelectorAll("h2, h3");
    if (!headings.length) {
      tocEl.innerHTML = '<p class="toc-empty">No sections yet.</p>';
      return;
    }
    headings.forEach(function (h, i) {
      if (!h.id) h.id = "toc-" + i + "-" + slugify(h.textContent || "section");
      const a = document.createElement("a");
      a.href = "#" + h.id;
      a.textContent = h.textContent;
      a.dataset.depth = h.tagName === "H3" ? "3" : "2";
      tocEl.appendChild(a);
    });
  }

  /**
   * Highlights the TOC entry for the section currently at the top of the reading area.
   */
  function bindTocScrollSpy(container) {
    if (tocSpyCleanup) {
      tocSpyCleanup();
      tocSpyCleanup = null;
    }
    if (!tocEl) return;
    const headings = container.querySelectorAll("h2, h3");
    if (!headings.length) return;

    /** Pixels from viewport top; ~sticky nav + small buffer. */
    const marginPx = 88;

    function update() {
      let activeId = headings[0].id;
      headings.forEach(function (h) {
        if (h.getBoundingClientRect().top <= marginPx) activeId = h.id;
      });
      tocEl.querySelectorAll("a").forEach(function (a) {
        const href = a.getAttribute("href");
        const isActive = href === "#" + activeId;
        a.classList.toggle("is-active", isActive);
        if (isActive) {
          a.setAttribute("aria-current", "location");
        } else {
          a.removeAttribute("aria-current");
        }
      });
    }

    let ticking = false;
    function onScrollOrResize() {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(function () {
          ticking = false;
          update();
        });
      }
    }

    window.addEventListener("scroll", onScrollOrResize, { passive: true });
    window.addEventListener("resize", onScrollOrResize);
    update();

    tocSpyCleanup = function () {
      window.removeEventListener("scroll", onScrollOrResize);
      window.removeEventListener("resize", onScrollOrResize);
      tocEl.querySelectorAll("a").forEach(function (a) {
        a.classList.remove("is-active");
        a.removeAttribute("aria-current");
      });
    };
  }

  function groupManifest(pages) {
    const groups = {};
    pages.forEach(function (p) {
      const m = p.match(/^content\/(phase-\d+)\//);
      const key = m ? m[1] : "Other";
      if (!groups[key]) groups[key] = [];
      groups[key].push(p);
    });
    return groups;
  }

  /** Sort paths by manifest order (stable when building week buckets). */
  function sortPathsByManifest(paths, orderMap) {
    return paths.slice().sort(function (a, b) {
      return (orderMap[a] ?? 1e9) - (orderMap[b] ?? 1e9);
    });
  }

  /**
   * Split a phase's pages into week sections (plus optional phase-level files like brownfield-project).
   */
  function sectionsForPhasePaths(phasePaths, orderMap) {
    const byWeek = {};
    const root = [];
    phasePaths.forEach(function (p) {
      const m = p.match(/^content\/phase-\d+\/week-(\d+)\//);
      if (m) {
        const w = m[1];
        if (!byWeek[w]) byWeek[w] = [];
        byWeek[w].push(p);
      } else {
        root.push(p);
      }
    });
    const sections = [];
    if (root.length) {
      sections.push({ kind: "root", label: "Phase resources", paths: sortPathsByManifest(root, orderMap) });
    }
    Object.keys(byWeek)
      .sort(function (a, b) {
        return Number(a) - Number(b);
      })
      .forEach(function (w) {
        sections.push({
          kind: "week",
          week: w,
          label: "Week " + w,
          paths: sortPathsByManifest(byWeek[w], orderMap),
        });
      });
    return sections;
  }

  function browseLabelForPath(path) {
    if (path === "content/syllabus.md") return "Syllabus";
    const segs = contentPathSegments(path);
    if (!segs.length) return labelForPath(path);
    const phaseRe = /^phase-(\d+)$/;
    const weekRe = /^week-(\d+)$/;
    if (segs.length >= 3 && phaseRe.test(segs[0]) && weekRe.test(segs[1])) {
      if (segs[2] === "labs") {
        if (segs[3] === "README") return "Labs guide";
        if (segs[3]) return humanizePathStem(segs[3]);
        return "Labs";
      }
      return humanizePathStem(segs[2]);
    }
    if (segs.length === 2 && phaseRe.test(segs[0])) {
      return humanizePathStem(segs[1]);
    }
    return labelForPath(path);
  }

  function phaseBrowseSummaryLabel(phaseKey) {
    if (phaseKey === "Other") return "Course";
    return phaseKey.replace(/^phase-/, "Phase ").replace(/-/g, " ");
  }

  function labelForPath(p) {
    if (p === "content/syllabus.md") return "Syllabus";
    const base = p.replace(/^content\//, "").replace(/\.md$/, "");
    return base.replace(/\//g, " · ");
  }

  function searchHaystackForPath(p) {
    const label = labelForPath(p);
    const flat = p.replace(/^content\//, "").replace(/\.md$/, "");
    return (label + " " + flat.replace(/\//g, " ")).toLowerCase();
  }

  /**
   * Fuzzy score: substring matches rank highest; otherwise subsequence match with bonuses
   * for consecutive chars and word/segment boundaries.
   */
  function fuzzyScore(query, hay) {
    const q = query.trim().toLowerCase();
    if (!q) return 0;
    const t = hay;
    const idx = t.indexOf(q);
    if (idx !== -1) {
      return 100000 - idx * 10 - (t.length - q.length) * 0.001;
    }
    let qi = 0;
    let score = 0;
    let last = -1;
    for (let i = 0; i < t.length && qi < q.length; i++) {
      if (t[i] === q[qi]) {
        const gap = last === -1 ? 0 : i - last - 1;
        score += 40 - Math.min(gap * 4, 35);
        if (last === i - 1) score += 20;
        const prev = t[i - 1];
        if (i === 0 || prev === " " || prev === "·" || prev === "-" || prev === "/") score += 6;
        last = i;
        qi++;
      }
    }
    if (qi < q.length) return -1;
    return score;
  }

  function runSearch(query) {
    const q = query.trim();
    if (!q) return [];
    const scored = [];
    searchIndex.forEach(function (entry) {
      const s = fuzzyScore(q, entry.hay);
      if (s >= 0) scored.push({ path: entry.path, score: s });
    });
    scored.sort(function (a, b) {
      return b.score - a.score;
    });
    return scored.slice(0, 20).map(function (x) {
      return x.path;
    });
  }

  function buildSearchIndex() {
    searchIndex = manifestPages.map(function (path) {
      return { path: path, hay: searchHaystackForPath(path) };
    });
  }

  function closeSearchPanel() {
    if (!searchPanel || !searchInput) return;
    searchPanel.hidden = true;
    searchInput.setAttribute("aria-expanded", "false");
    searchInput.removeAttribute("aria-activedescendant");
    searchActiveIdx = -1;
  }

  function openSearchPanel() {
    if (!searchPanel || !searchInput) return;
    searchPanel.hidden = false;
    searchInput.setAttribute("aria-expanded", "true");
  }

  function updateSearchHighlight() {
    if (!searchListbox) return;
    const opts = searchListbox.querySelectorAll('button[role="option"]');
    opts.forEach(function (btn, i) {
      btn.classList.toggle("is-active", i === searchActiveIdx);
    });
    if (searchActiveIdx >= 0 && opts[searchActiveIdx]) {
      searchInput.setAttribute("aria-activedescendant", opts[searchActiveIdx].id);
    } else {
      searchInput.removeAttribute("aria-activedescendant");
    }
  }

  function refreshSearchUI() {
    if (!searchInput || !searchListbox) return;
    const q = searchInput.value;
    lastSearchPaths = runSearch(q);
    if (!q.trim()) {
      searchListbox.innerHTML = "";
      closeSearchPanel();
      return;
    }
    if (!lastSearchPaths.length) {
      searchListbox.innerHTML =
        '<li class="site-nav__search-empty" role="presentation">No matching pages.</li>';
      searchActiveIdx = -1;
      openSearchPanel();
      return;
    }
    let html = "";
    lastSearchPaths.forEach(function (path, i) {
      const optId = "site-search-opt-" + i;
      html +=
        '<li role="presentation">' +
        '<button type="button" role="option" id="' +
        escapeAttr(optId) +
        '" class="site-nav__search-option" data-path="' +
        escapeAttr(path) +
        '">' +
        '<span class="site-nav__search-option__title">' +
        escapeHtml(labelForPath(path)) +
        "</span>" +
        '<span class="site-nav__search-option__path">' +
        escapeHtml(path) +
        "</span>" +
        "</button></li>";
    });
    searchListbox.innerHTML = html;
    searchActiveIdx = 0;
    searchListbox.querySelectorAll("button[data-path]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const p = btn.getAttribute("data-path");
        if (!p) return;
        closeSearchPanel();
        searchInput.value = "";
        navigateTo(p);
      });
    });
    openSearchPanel();
    updateSearchHighlight();
  }

  function bindSiteSearch() {
    if (!searchInput || !searchPanel || !searchListbox || !searchWrap) return;

    searchInput.addEventListener("input", function () {
      refreshSearchUI();
    });

    searchInput.addEventListener("focus", function () {
      if (searchInput.value.trim()) refreshSearchUI();
    });

    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        if (searchPanel.hidden && searchInput.value.trim()) {
          refreshSearchUI();
          updateSearchHighlight();
          return;
        }
        const opts = searchListbox.querySelectorAll('button[role="option"]');
        const n = opts.length;
        if (!n) return;
        searchActiveIdx = Math.min(
          (searchActiveIdx < 0 ? -1 : searchActiveIdx) + 1,
          n - 1
        );
        if (searchActiveIdx < 0) searchActiveIdx = 0;
        updateSearchHighlight();
        return;
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        if (searchPanel.hidden && searchInput.value.trim()) {
          refreshSearchUI();
          const opts = searchListbox.querySelectorAll('button[role="option"]');
          const n = opts.length;
          searchActiveIdx = n ? n - 1 : -1;
          updateSearchHighlight();
          return;
        }
        const opts = searchListbox.querySelectorAll('button[role="option"]');
        const n = opts.length;
        if (!n) return;
        searchActiveIdx = Math.max((searchActiveIdx < 0 ? n : searchActiveIdx) - 1, 0);
        updateSearchHighlight();
        return;
      }
      if (e.key === "Enter") {
        if (searchPanel.hidden || searchActiveIdx < 0 || !lastSearchPaths[searchActiveIdx]) return;
        e.preventDefault();
        const p = lastSearchPaths[searchActiveIdx];
        closeSearchPanel();
        searchInput.value = "";
        navigateTo(p);
        return;
      }
      if (e.key === "Escape") {
        if (!searchPanel.hidden) {
          e.preventDefault();
          closeSearchPanel();
        }
      }
    });

    document.addEventListener("click", function (e) {
      if (!searchWrap.contains(e.target)) closeSearchPanel();
    });

    searchListbox.addEventListener("mousedown", function (e) {
      if (e.target.closest("button[data-path]")) e.preventDefault();
    });

    document.addEventListener("keydown", function (e) {
      if (e.code !== "KeyK") return;
      if (!(e.metaKey || e.ctrlKey)) return;
      const t = e.target;
      if (t && (t.tagName === "TEXTAREA" || t.isContentEditable)) return;
      e.preventDefault();
      searchInput.focus();
      if (typeof searchInput.select === "function") searchInput.select();
    });
  }

  function renderBrowse(groups) {
    const orderMap = {};
    manifestPages.forEach(function (p, i) {
      orderMap[p] = i;
    });
    const phaseOrder = Object.keys(groups).sort();
    let html = "";
    phaseOrder.forEach(function (phase) {
      const items = groups[phase];
      const isPhase = /^phase-\d+$/.test(phase);
      const curPhase = currentPagePath.match(/^content\/(phase-\d+)\//);
      const open = isPhase && curPhase && curPhase[1] === phase ? " open" : "";
      html += "<details" + open + ">";
      html += "<summary>" + escapeHtml(phaseBrowseSummaryLabel(phase)) + "</summary>";
      html += '<div class="browse__phase-body">';
      if (isPhase) {
        sectionsForPhasePaths(items, orderMap).forEach(function (section, secIdx) {
          html += '<section class="browse__section">';
          html +=
            '<p class="browse__section-label" id="browse-' +
            escapeAttr(phase + "-" + secIdx) +
            '">' +
            escapeHtml(section.label) +
            "</p>";
          html += "<ul>";
          section.paths.forEach(function (path) {
            const active = path === currentPagePath ? ' aria-current="page"' : "";
            html +=
              '<li><a href="' +
              pageUrl(path) +
              '"' +
              active +
              ">" +
              escapeHtml(browseLabelForPath(path)) +
              "</a></li>";
          });
          html += "</ul></section>";
        });
      } else {
        html += "<ul>";
        sortPathsByManifest(items, orderMap).forEach(function (path) {
          const active = path === currentPagePath ? ' aria-current="page"' : "";
          html +=
            '<li><a href="' +
            pageUrl(path) +
            '"' +
            active +
            ">" +
            escapeHtml(browseLabelForPath(path)) +
            "</a></li>";
        });
        html += "</ul>";
      }
      html += "</div></details>";
    });
    browseEl.innerHTML = html;
    browseEl.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        closeFab();
      });
    });
  }

  function escapeHtml(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  /** Path segments under content/, without .md (e.g. phase-1/week-1/day-1). */
  function contentPathSegments(path) {
    const rel = path.replace(/^content\//, "").replace(/\.md$/, "");
    return rel.split("/").filter(Boolean);
  }

  function humanizePathStem(stem) {
    if (stem === "week-overview") return "Week overview";
    const day = /^day-(\d+)$/.exec(stem);
    if (day) return "Day " + day[1];
    const lab = /^lab-(\d+)$/.exec(stem);
    if (lab) return "Lab " + lab[1];
    return stem
      .split("-")
      .map(function (w) {
        return w ? w.charAt(0).toUpperCase() + w.slice(1) : "";
      })
      .join(" ");
  }

  /**
   * Breadcrumb trail for course URLs: phase → week → day / labs / week overview / etc.
   * Each segment except the last links to a sensible parent page.
   */
  function buildBreadcrumbItems(path) {
    const root = { label: "Course", href: DEFAULT_PAGE };
    if (!isAllowedPath(path)) {
      return [root, { label: "Not found", href: null }];
    }
    if (path === "content/syllabus.md") {
      return [root, { label: "Syllabus", href: null }];
    }

    const segs = contentPathSegments(path);
    if (!segs.length) {
      return [root, { label: labelForPath(path), href: null }];
    }

    const items = [root];
    const phaseRe = /^phase-(\d+)$/;
    const weekRe = /^week-(\d+)$/;

    if (!phaseRe.test(segs[0])) {
      items.push({ label: humanizePathStem(segs[segs.length - 1]) || labelForPath(path), href: null });
      return items;
    }

    const phaseDir = segs[0];
    const phaseNum = phaseRe.exec(segs[0])[1];
    items.push({
      label: "Phase " + phaseNum,
      href: "content/" + phaseDir + "/week-1/day-1.md",
    });

    if (segs.length === 2 && !weekRe.test(segs[1])) {
      items.push({ label: humanizePathStem(segs[1]), href: null });
      return items;
    }

    if (segs.length < 2 || !weekRe.test(segs[1])) {
      items.push({ label: labelForPath(path), href: null });
      return items;
    }

    const weekDir = segs[1];
    const weekNum = weekRe.exec(segs[1])[1];
    const weekBase = "content/" + phaseDir + "/" + weekDir;
    items.push({
      label: "Week " + weekNum,
      href: weekBase + "/week-overview.md",
    });

    if (segs.length === 2) {
      items[items.length - 1] = { label: "Week " + weekNum, href: null };
      return items;
    }

    if (segs[2] === "labs") {
      const labsReadme = weekBase + "/labs/README.md";
      if (segs.length < 4) {
        items.push({ label: "Labs", href: null });
        return items;
      }
      const fileStem = segs[3];
      if (fileStem === "README") {
        items.push({ label: "Labs", href: null });
        return items;
      }
      items.push({ label: "Labs", href: labsReadme });
      items.push({ label: humanizePathStem(fileStem), href: null });
      return items;
    }

    items.push({ label: humanizePathStem(segs[2]), href: null });
    return items;
  }

  function renderBreadcrumb(path) {
    if (!breadcrumbEl) return;
    const items = buildBreadcrumbItems(path);
    let html = '<ol class="breadcrumb__list">';
    items.forEach(function (item, i) {
      const isLast = i === items.length - 1;
      const isSelfLink = !!(item.href && path === item.href && !isLast);
      if (isLast) {
        html +=
          '<li class="breadcrumb__item" aria-current="page">' + escapeHtml(item.label) + "</li>";
      } else if (item.href && !isSelfLink) {
        html +=
          '<li class="breadcrumb__item"><a href="' +
          escapeAttr(pageUrl(item.href)) +
          '">' +
          escapeHtml(item.label) +
          "</a></li>";
      } else {
        html +=
          '<li class="breadcrumb__item"><span class="breadcrumb__text">' +
          escapeHtml(item.label) +
          "</span></li>";
      }
    });
    html += "</ol>";
    breadcrumbEl.innerHTML = html;
  }

  function renderFabNav(groups) {
    fabNavEl.innerHTML = browseEl.innerHTML;
    fabNavEl.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        closeFab();
      });
    });
  }

  function openFab() {
    fabPanel.hidden = false;
    fab.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  }

  function closeFab() {
    fabPanel.hidden = true;
    fab.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }

  function onArticleClick(e) {
    const a = e.target.closest("a");
    if (!a) return;
    const href = a.getAttribute("href");
    if (!href) return;
    const resolved = resolveMdHref(href, currentPagePath);
    if (resolved) {
      e.preventDefault();
      navigateTo(resolved);
    }
  }

  function navigateTo(path) {
    if (!isAllowedPath(path)) {
      showStatus("Invalid page path.", 4000);
      return;
    }
    const u = new URL(window.location.href);
    u.searchParams.set("page", path);
    window.history.pushState({ page: path }, "", u.pathname + u.search);
    loadPage(path);
  }

  function bindScrollTitle() {
    const onScroll = function () {
      const y = window.scrollY;
      const t = Math.min(1, y / 420);
      const w = Math.round(800 - t * 100);
      titleEl.style.fontWeight = String(Math.max(700, Math.min(800, w)));
      titleEl.style.transform = "translateY(" + t * 3 + "px)";
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  async function loadManifest() {
    try {
      const res = await fetch(new URL("content/manifest.json", INDEX_DIR), FETCH_DOC);
      if (!res.ok) return;
      const data = await res.json();
      manifestPages = Array.isArray(data.pages) ? data.pages : [];
    } catch {
      manifestPages = [];
    }
    buildSearchIndex();
  }

  async function loadPage(path) {
    const seq = ++loadPageSeq;
    if (tocSpyCleanup) {
      tocSpyCleanup();
      tocSpyCleanup = null;
    }
    currentPagePath = path;
    renderBreadcrumb(path);
    titleEl.textContent = "Loading…";
    articleEl.innerHTML = "";
    clearSidebarRail();

    if (!isAllowedPath(path)) {
      articleEl.innerHTML =
        '<p class="prose prose--error">Invalid or missing page. Open the <a href="' +
        pageUrl(DEFAULT_PAGE) +
        '">syllabus</a>.</p>';
      titleEl.textContent = "Not found";
      return;
    }

    let text;
    try {
      const res = await fetch(new URL(path, INDEX_DIR), FETCH_DOC);
      if (seq !== loadPageSeq) return;
      if (!res.ok) throw new Error(String(res.status));
      text = await res.text();
      if (seq !== loadPageSeq) return;
    } catch (err) {
      if (seq !== loadPageSeq) return;
      articleEl.innerHTML =
        '<p class="prose prose--error">Could not load this page. <a href="' +
        pageUrl(DEFAULT_PAGE) +
        '">Return to syllabus</a>.</p>';
      titleEl.textContent = "Error";
      showStatus("Failed to load document.", 4000);
      return;
    }

    if (seq !== loadPageSeq) return;

    if (typeof marked === "undefined") {
      articleEl.textContent = text;
      titleEl.textContent = path;
      return;
    }

    const html = marked.parse(preprocessMarkdownComponents(text));
    articleEl.innerHTML = html;
    applyArticleLinkTargets(articleEl);
    await hydrateMarkdownComponents(articleEl, seq);
    if (seq !== loadPageSeq) return;
    hydrateLinks(articleEl, seq);
    if (seq !== loadPageSeq) return;
    applyArticleLinkTargets(articleEl);
    if (seq !== loadPageSeq) return;
    moveLinksToSidebar(articleEl, seq);
    if (seq !== loadPageSeq) return;
    hydrateChecklists(articleEl, seq);
    if (seq !== loadPageSeq) return;
    moveChecklistsToSidebar(articleEl, seq);
    if (seq !== loadPageSeq) return;
    updateSidebarRailVisibility();
    if (seq !== loadPageSeq) return;

    const h1 = articleEl.querySelector("h1");
    if (h1) {
      titleEl.textContent = h1.textContent;
      h1.classList.add("is-mirrored");
    } else {
      titleEl.textContent = labelForPath(path);
    }

    buildToc(articleEl);
    bindTocScrollSpy(articleEl);
    document.title = titleEl.textContent + " — Applied AI";

    const groups = groupManifest(manifestPages.length ? manifestPages : [path]);
    renderBrowse(groups);
    renderFabNav(groups);

    showStatus("Loaded", 1200);
  }

  async function init() {
    initThemeToggle();
    await loadManifest();
    bindSiteSearch();
    const q = getQueryPage();
    const path = q && isAllowedPath(q) ? q : DEFAULT_PAGE;
    currentPagePath = path;
    if (!q || !isAllowedPath(q)) {
      const u = new URL(window.location.href);
      u.searchParams.set("page", path);
      window.history.replaceState({ page: path }, "", u.pathname + u.search);
    }
    articleEl.addEventListener("click", onArticleClick);
    if (sidebarChecklistRailEl) sidebarChecklistRailEl.addEventListener("click", onArticleClick);
    window.addEventListener("popstate", function () {
      const p = getQueryPage();
      loadPage(p && isAllowedPath(p) ? p : DEFAULT_PAGE);
    });

    if (fab && fabPanel) {
      fab.addEventListener("click", function () {
        if (fabPanel.hidden) openFab();
        else closeFab();
      });
      fabClose.addEventListener("click", closeFab);
      fabPanel.addEventListener("click", function (e) {
        if (e.target === fabPanel) closeFab();
      });
    }

    bindScrollTitle();
    await loadPage(path);
  }

  init();
})();
