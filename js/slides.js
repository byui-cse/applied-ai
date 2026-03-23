/**
 * Inline slide deck: fetch JSON under content/…/slides/, render with navigation + fullscreen.
 */
(function () {
  "use strict";

  var FETCH_DOC = { cache: "no-store" };

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  function parseMarkdown(md) {
    if (typeof marked !== "undefined" && typeof marked.parse === "function") {
      return marked.parse(String(md || ""));
    }
    return "<p>" + escapeHtml(String(md || "")) + "</p>";
  }

  /** Directory URL for the slide JSON file (for resolving relative image paths). */
  function jsonDirHref(jsonPath, indexDir) {
    var u = new URL(jsonPath, indexDir);
    u.pathname = u.pathname.replace(/[^/]+$/, "");
    return u.href;
  }

  /**
   * Resolve relative <img src> against the JSON folder so markdown like
   * ![alt](images/foo.png) works on GitHub Pages.
   */
  function resolveSlideImageUrls(html, jsonPath, indexDir) {
    var base;
    try {
      base = jsonDirHref(jsonPath, indexDir);
    } catch {
      return html;
    }
    try {
      var doc = new DOMParser().parseFromString(html, "text/html");
      var imgs = doc.querySelectorAll("img[src]");
      imgs.forEach(function (img) {
        var src = img.getAttribute("src");
        if (!src || /^data:/i.test(src)) return;
        if (/^https?:\/\//i.test(src)) return;
        try {
          img.setAttribute("src", new URL(src, base).href);
        } catch {
          /* keep original */
        }
      });
      return doc.body.innerHTML;
    } catch {
      return html;
    }
  }

  function parseSlideMarkdown(md, jsonPath, indexDir) {
    return resolveSlideImageUrls(parseMarkdown(md), jsonPath, indexDir);
  }

  function renderSlides(container, data, jsonPath, indexDir) {
    var deckTitle = data.title || "Slides";
    var subtitle = data.subtitle || "";
    var slides = Array.isArray(data.slides) ? data.slides : [];

    if (!slides.length) {
      container.innerHTML =
        '<p class="slides__empty prose">No slides in this deck.</p>';
      return;
    }

    var uid =
      "slides-" +
      Math.random().toString(36).slice(2, 10);

    var html = "";
    html +=
      '<div class="slides" id="' +
      uid +
      '" role="region" aria-roledescription="carousel" aria-label="' +
      escapeHtml(deckTitle) +
      '">';
    html += '<div class="slides__chrome">';
    html += '<div class="slides__head">';
    html += '<p class="slides__label">Slides</p>';
    html += '<p class="slides__title">' + escapeHtml(deckTitle) + "</p>";
    if (subtitle) {
      html += '<p class="slides__subtitle">' + escapeHtml(subtitle) + "</p>";
    }
    html += "</div>";
    html += '<div class="slides__toolbar">';
    html +=
      '<span class="slides__counter" aria-live="polite"><span class="slides__counter-current">1</span><span class="slides__counter-sep">/</span><span class="slides__counter-total">' +
      slides.length +
      "</span></span>";
    html +=
      '<button type="button" class="slides__btn slides__btn--fs" aria-pressed="false" title="Full screen (F)">';
    html +=
      '<span class="slides__btn-icon" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/></svg></span>';
    html += '<span class="slides__btn-text">Full screen</span>';
    html += "</button>";
    html += "</div>";
    html += "</div>";

    html += '<div class="slides__viewport">';
    html +=
      '<div class="slides__track" tabindex="0" role="group" aria-label="Slide content">';
    html +=
      '<div class="slides__strip" style="--slides-n: ' +
      slides.length +
      '" data-slide-count="' +
      slides.length +
      '">';

    slides.forEach(function (slide, i) {
      var st = slide.title ? String(slide.title) : "";
      var md = slide.markdown != null ? String(slide.markdown) : "";
      var labelled = st ? escapeHtml(st) : "Slide " + (i + 1);
      var ariah = i === 0 ? "false" : "true";
      html +=
        '<article class="slides__slide prose" data-slide-index="' +
        i +
        '" aria-label="' +
        labelled +
        '" aria-hidden="' +
        ariah +
        '" role="group">';
      if (st) {
        html += '<h2 class="slides__slide-title">' + escapeHtml(st) + "</h2>";
      }
      html +=
        '<div class="slides__slide-body">' +
        parseSlideMarkdown(md, jsonPath, indexDir) +
        "</div>";
      html += "</article>";
    });

    html += "</div>";
    html += "</div>";
    html += '<div class="slides__nav">';
    html += '<div class="slides__nav-side slides__nav-side--start">';
    html +=
      '<button type="button" class="slides__btn slides__btn--prev" aria-label="Previous slide">';
    html += "Previous";
    html += "</button>";
    html += "</div>";
    html += '<div class="slides__dots" role="tablist" aria-label="Slides">';
    slides.forEach(function (_s, di) {
      var sel = di === 0 ? ' aria-selected="true"' : ' aria-selected="false"';
      html +=
        '<button type="button" class="slides__dot" role="tab" tabindex="-1"' +
        sel +
        ' data-dot="' +
        di +
        '" aria-label="Go to slide ' +
        (di + 1) +
        '"></button>';
    });
    html += "</div>";
    html += '<div class="slides__nav-side slides__nav-side--end">';
    html +=
      '<button type="button" class="slides__btn slides__btn--next" aria-label="Next slide">';
    html += "Next";
    html += "</button>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";

    container.innerHTML = html;

    var root = container.querySelector(".slides");
    var track = container.querySelector(".slides__track");
    var strip = container.querySelector(".slides__strip");
    var articles = container.querySelectorAll(".slides__slide");
    var btnPrev = container.querySelector(".slides__btn--prev");
    var btnNext = container.querySelector(".slides__btn--next");
    var btnFs = container.querySelector(".slides__btn--fs");
    var counterCur = container.querySelector(".slides__counter-current");
    var dots = container.querySelectorAll(".slides__dot");
    var viewport = container.querySelector(".slides__viewport");

    var index = 0;
    var slideCount = articles.length;

    if (
      typeof window !== "undefined" &&
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ) {
      root.classList.add("slides--reduced-motion");
    }

    function syncStrip() {
      if (!strip || !slideCount) return;
      var pct = (index / slideCount) * 100;
      strip.style.transform = "translateX(-" + pct + "%)";
    }

    function setIndex(n) {
      var max = slideCount - 1;
      n = Math.max(0, Math.min(max, n));
      index = n;
      syncStrip();
      articles.forEach(function (el, j) {
        el.setAttribute("aria-hidden", j !== index ? "true" : "false");
      });
      dots.forEach(function (d, j) {
        d.setAttribute("aria-selected", j === index ? "true" : "false");
        d.classList.toggle("is-active", j === index);
      });
      if (counterCur) counterCur.textContent = String(index + 1);
      if (btnPrev) {
        var prevConcealed = index === 0;
        btnPrev.classList.toggle("slides__btn--visually-hidden", prevConcealed);
        if (prevConcealed) {
          btnPrev.setAttribute("aria-hidden", "true");
          btnPrev.setAttribute("tabindex", "-1");
        } else {
          btnPrev.removeAttribute("aria-hidden");
          btnPrev.removeAttribute("tabindex");
        }
      }
      if (btnNext) btnNext.hidden = index >= max;
    }

    function goPrev() {
      if (index <= 0) return;
      setIndex(index - 1);
    }
    function goNext() {
      if (index >= slideCount - 1) return;
      setIndex(index + 1);
    }

    if (btnPrev) btnPrev.addEventListener("click", goPrev);
    if (btnNext) btnNext.addEventListener("click", goNext);

    dots.forEach(function (dot) {
      dot.addEventListener("click", function () {
        var di = parseInt(dot.getAttribute("data-dot") || "0", 10);
        if (!isNaN(di)) setIndex(di);
      });
    });

    function onFullscreenArrows(e) {
      if (document.fullscreenElement !== root) return;
      var el = e.target;
      if (
        el &&
        (el.tagName === "TEXTAREA" ||
          el.tagName === "INPUT" ||
          (el.isContentEditable && el.isContentEditable))
      ) {
        return;
      }
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        e.stopPropagation();
        if (index > 0) goPrev();
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        e.stopPropagation();
        if (index < slideCount - 1) goNext();
      }
    }

    document.addEventListener("keydown", onFullscreenArrows, true);

    if (track) {
      track.addEventListener("keydown", function (e) {
        if (document.fullscreenElement === root) return;
        if (e.key === "ArrowLeft" || e.key === "PageUp") {
          e.preventDefault();
          if (index > 0) goPrev();
        } else if (
          e.key === "ArrowRight" ||
          e.key === "PageDown" ||
          e.key === " "
        ) {
          e.preventDefault();
          if (index < slideCount - 1) goNext();
        } else if (e.key === "Home") {
          e.preventDefault();
          setIndex(0);
        } else if (e.key === "End") {
          e.preventDefault();
          setIndex(articles.length - 1);
        } else if (e.key === "f" || e.key === "F") {
          e.preventDefault();
          toggleFs();
        }
      });
    }

    function isFs() {
      return document.fullscreenElement === root;
    }

    function toggleFs() {
      if (!root) return;
      if (!document.fullscreenEnabled) return;
      if (isFs()) {
        document.exitFullscreen().catch(function () {});
      } else {
        root.requestFullscreen().catch(function () {});
      }
    }

    function syncFsButton() {
      if (!btnFs) return;
      var on = isFs();
      btnFs.setAttribute("aria-pressed", on ? "true" : "false");
      var t = on ? "Exit full screen (F)" : "Full screen (F)";
      btnFs.setAttribute("title", t);
      var txt = btnFs.querySelector(".slides__btn-text");
      if (txt) txt.textContent = on ? "Exit full screen" : "Full screen";
    }

    function onFullscreenChange() {
      if (!root) return;
      if (document.fullscreenElement === root) {
        root.classList.add("slides--fullscreen");
      } else {
        root.classList.remove("slides--fullscreen");
      }
      syncFsButton();
    }

    if (btnFs && document.fullscreenEnabled) {
      btnFs.addEventListener("click", toggleFs);
      document.addEventListener("fullscreenchange", onFullscreenChange);
    } else if (btnFs) {
      btnFs.hidden = true;
    }

    setIndex(0);
    syncFsButton();

    if (viewport && track) {
      viewport.addEventListener("click", function (e) {
        if (e.target.closest("a, button")) return;
        track.focus();
      });
    }
  }

  function mount(container, jsonPath, indexDir) {
    if (!container || !jsonPath) return;
    container.innerHTML = '<p class="slides__loading">Loading slides…</p>';
    var url;
    try {
      url = new URL(jsonPath, indexDir);
    } catch {
      container.innerHTML =
        '<p class="prose prose--error">Invalid slides URL.</p>';
      return;
    }
    fetch(url, FETCH_DOC)
      .then(function (res) {
        if (!res.ok) throw new Error(String(res.status));
        return res.json();
      })
      .then(function (data) {
        renderSlides(container, data, jsonPath, indexDir);
      })
      .catch(function () {
        container.innerHTML =
          '<p class="prose prose--error">Could not load slides.</p>';
      });
  }

  window.AppliedAISlides = { mount: mount };
})();
