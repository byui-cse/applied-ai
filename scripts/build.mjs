import fs from "fs";
import path from "path";

const ROOT = process.cwd();
const CONTENT_DIR = path.join(ROOT, "content");
const PAGES_DIR = path.join(ROOT, "pages");

const COURSE_TITLE = "Applied AI for Software Development";
const COURSE_SUBTITLE = "A 14-week applied course for real-world engineering work";

const MODULE_TITLES = {
  "module-1": "1. Context & Efficiency",
  "module-2": "2. Architectural State",
  "module-3": "3. Extended Tools",
  "module-4": "4. Foundations & Skills",
  "module-5": "5. Extensibility",
  "module-6": "6. Autonomous Agents",
  "module-7": "7. Advanced Workflows"
};

const PHASE_TITLES = {
  "phase-1": "Phase 1: Brownfield (Legacy Systems)",
  "phase-2": "Phase 2: Greenfield (New Systems)"
};

function ensureDir(dirPath){
  fs.mkdirSync(dirPath, { recursive: true });
}

function escapeHtml(s){
  return s
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function inlineMarkdown(raw){
  // Minimal inline support: links, inline code, bold and italics.
  let s = escapeHtml(raw);

  // Inline code: `code`
  s = s.replace(/`([^`]+)`/g, (_m, code) => `<code>${code}</code>`);

  // Links: [text](url)
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, text, url) => {
    return `<a href="${url}" target="_blank" rel="noopener noreferrer">${text}</a>`;
  });

  // Bold: **text**
  s = s.replace(/\*\*([^*]+)\*\*/g, (_m, t) => `<strong>${t}</strong>`);

  // Italic: *text*
  s = s.replace(/(^|[^*])\*([^*]+)\*/g, (_m, prefix, t) => `${prefix}<em>${t}</em>`);

  return s;
}

function markdownToHtml(md){
  const lines = md.replace(/\r\n/g, "\n").split("\n");
  const out = [];
  let i = 0;
  let paragraphLines = [];

  const flushParagraph = () => {
    if(paragraphLines.length === 0) return;
    const joined = paragraphLines.join(" ").trim();
    if(joined.length > 0){
      out.push(`<p>${inlineMarkdown(joined)}</p>`);
    }
    paragraphLines = [];
  };

  const peek = () => lines[i] ?? "";

  while(i < lines.length){
    const line = peek();
    const trimmed = line.trim();

    if(trimmed === ""){
      flushParagraph();
      i++;
      continue;
    }

    // Fenced code blocks
    if(trimmed.startsWith("```")){
      flushParagraph();
      const lang = trimmed.slice(3).trim();
      i++;
      const codeLines = [];
      while(i < lines.length && !lines[i].trim().startsWith("```")){
        codeLines.push(lines[i]);
        i++;
      }
      // consume closing fence if present
      if(i < lines.length && lines[i].trim().startsWith("```")) i++;
      const code = escapeHtml(codeLines.join("\n"));
      const langClass = lang ? ` class="language-${escapeHtml(lang)}"` : "";
      out.push(`<pre><code${langClass}>${code}</code></pre>`);
      continue;
    }

    // Horizontal rule
    if(/^---+$/.test(trimmed)){
      flushParagraph();
      out.push("<hr />");
      i++;
      continue;
    }

    // Headings
    const headingMatch = trimmed.match(/^(#{1,6})\s+(.+)$/);
    if(headingMatch){
      flushParagraph();
      const level = headingMatch[1].length;
      const text = headingMatch[2];
      out.push(`<h${level}>${inlineMarkdown(text)}</h${level}>`);
      i++;
      continue;
    }

    // Blockquotes
    if(trimmed.startsWith(">")){
      flushParagraph();
      const quoteLines = [];
      while(i < lines.length && (lines[i].trim().startsWith(">") || lines[i].trim() === "")){
        if(lines[i].trim() === ""){
          i++;
          continue;
        }
        quoteLines.push(lines[i].trim().replace(/^>\s?/, ""));
        i++;
      }
      const quoteHtml = quoteLines.map((l) => `<p>${inlineMarkdown(l)}</p>`).join("");
      out.push(`<blockquote>${quoteHtml}</blockquote>`);
      continue;
    }

    // Unordered lists
    if(/^[-*]\s+/.test(trimmed)){
      flushParagraph();
      const items = [];
      while(i < lines.length && /^[-*]\s+/.test(lines[i].trim())){
        const m = lines[i].trim().match(/^[-*]\s+(.+)$/);
        if(m) items.push(m[1]);
        i++;
      }
      const lis = items.map((t) => `<li>${inlineMarkdown(t)}</li>`).join("");
      out.push(`<ul>${lis}</ul>`);
      continue;
    }

    // Ordered lists
    if(/^\d+\.\s+/.test(trimmed)){
      flushParagraph();
      const items = [];
      while(i < lines.length && /^\d+\.\s+/.test(lines[i].trim())){
        const m = lines[i].trim().match(/^\d+\.\s+(.+)$/);
        if(m) items.push(m[1]);
        i++;
      }
      const lis = items.map((t) => `<li>${inlineMarkdown(t)}</li>`).join("");
      out.push(`<ol>${lis}</ol>`);
      continue;
    }

    // Default: accumulate paragraphs
    paragraphLines.push(line);
    i++;
  }

  flushParagraph();
  return out.join("\n");
}

function walkMarkdown(dir){
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];
  for(const ent of entries){
    const p = path.join(dir, ent.name);
    if(ent.isDirectory()){
      files.push(...walkMarkdown(p));
    }else if(ent.isFile() && p.endsWith(".md")){
      files.push(p);
    }
  }
  return files;
}

function relUrl(fromFile, toPath){
  const rel = path.relative(path.dirname(fromFile), toPath);
  return rel.split(path.sep).join("/");
}

function getFirstHeading(md){
  const m = md.match(/^#\s+(.+)$/m);
  return m ? m[1].trim() : null;
}

function buildNavStructure(weekMarkdownRelPaths){
  // weekMarkdownRelPaths like: phase-1/module-1/week-1.md
  const phaseOrder = ["phase-1", "phase-2"];
  const moduleOrder = ["module-1","module-2","module-3","module-4","module-5","module-6","module-7"];

  const structure = {};
  for(const rp of weekMarkdownRelPaths){
    const parts = rp.split(path.sep);
    const phase = parts[0];
    const module = parts[1];
    const file = parts[2]; // week-X.md
    const weekMatch = file.match(/^week-(\d+)\.md$/);
    const weekNum = weekMatch ? Number(weekMatch[1]) : null;
    if(!weekNum) continue;
    structure[phase] ??= {};
    structure[phase][module] ??= [];
    structure[phase][module].push({ weekNum, relPath: rp });
  }

  for(const phase of Object.keys(structure)){
    for(const module of Object.keys(structure[phase])){
      structure[phase][module].sort((a,b) => a.weekNum - b.weekNum);
    }
  }

  return { structure, phaseOrder, moduleOrder };
}

function markdownRelToOutput(relPath){
  // content/phase-1/module-1/week-1.md => pages/phase-1/module-1/week-1/index.html
  const parts = relPath.split(path.sep);
  const phase = parts[0];
  const module = parts[1];
  const file = parts[2]; // week-X.md
  const outDirName = file.replace(/\.md$/,"");
  return path.join(PAGES_DIR, phase, module, outDirName, "index.html");
}

function markdownRelToOutputDir(relPath){
  // same as markdownRelToOutput, but output directory path without index.html
  const parts = relPath.split(path.sep);
  const phase = parts[0];
  const module = parts[1];
  const file = parts[2];
  const outDirName = file.replace(/\.md$/,"");
  return path.join(PAGES_DIR, phase, module, outDirName);
}

function markdownRelToLabOutput(relPath){
  // content/phase-1/module-1/labs/week-1-context-management.md
  // => pages/phase-1/module-1/labs/week-1-context-management/index.html
  const parts = relPath.split(path.sep);
  const phase = parts[0];
  const module = parts[1];
  const file = parts[3]; // week-*.md
  const outDirName = file.replace(/\.md$/,"");
  return path.join(PAGES_DIR, phase, module, "labs", outDirName, "index.html");
}

function renderPage({ fromOutputFile, title, contentHtml, navHtml }){
  const stylesHref = relUrl(fromOutputFile, path.join(ROOT, "assets", "styles.css"));
  const appHref = relUrl(fromOutputFile, path.join(ROOT, "assets", "app.js"));
  const syllabusHref = relUrl(fromOutputFile, path.join(ROOT, "syllabus.html"));
  const homeHref = relUrl(fromOutputFile, path.join(ROOT, "index.html"));

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${escapeHtml(title)}</title>
  <link rel="stylesheet" href="${stylesHref}" />
  <script defer src="${appHref}"></script>
</head>
<body>
  <a id="skipToContent" class="skipLink" href="#mainContent">Skip to content</a>
  <header class="siteHeader">
    <div class="headerInner">
      <button id="sidebarToggle" class="iconBtn" type="button" aria-label="Toggle navigation" aria-controls="siteNav" aria-expanded="false">☰</button>
      <div class="brand">
        <a class="brandLink" href="${homeHref}">${escapeHtml(COURSE_TITLE)}</a>
        <span class="brandSub">${escapeHtml(COURSE_SUBTITLE)}</span>
      </div>
      <div class="headerActions">
        <a class="pill" href="${syllabusHref}">Syllabus</a>
        <button id="themeToggle" class="pill" type="button" aria-label="Toggle theme" aria-pressed="false">Theme</button>
      </div>
    </div>
  </header>

  <div class="layout">
    ${navHtml}
    <main class="content" id="mainContent">
      <article class="prose">
        ${contentHtml}
      </article>
    </main>
  </div>
</body>
</html>`;
}

function buildNavHtml({ fromOutputFile, navData }){
  const { structure, phaseOrder, moduleOrder } = navData;

  const linkToDir = (targetDir) => {
    const rel = path.relative(path.dirname(fromOutputFile), targetDir);
    if(rel === ""){
      return "./";
    }
    return rel.split(path.sep).join("/") + "/";
  };
  const indexRel = relUrl(fromOutputFile, path.join(ROOT, "index.html"));

  let html = `<nav class="sidebar" id="siteNav">
  <div class="sidebarNav">`;

  html += `<a class="navLink" data-nav-link="true" href="${indexRel}" style="margin-bottom:6px;">Course Home</a>`;

  for(const phase of phaseOrder){
    if(!structure[phase]) continue;
    html += `<div class="navSectionTitle">${escapeHtml(PHASE_TITLES[phase])}</div>`;
    // modules within phase
    const modulesInPhase = Object.keys(structure[phase]).sort((a,b) => moduleOrder.indexOf(a) - moduleOrder.indexOf(b));
    for(const module of modulesInPhase){
      const weeks = structure[phase][module] ?? [];
      const moduleTitle = MODULE_TITLES[module] ?? module;
      html += `<div class="navModuleTitle">${escapeHtml(moduleTitle)}</div>`;
      html += `<div class="navWeek">`;
      for(const w of weeks){
        const outDir = markdownRelToOutputDir(w.relPath);
        const href = linkToDir(outDir);
        html += `<a class="navLink" data-nav-link="true" href="${href}">Week ${w.weekNum}</a>`;
      }
      html += `</div>`;
    }
  }

  html += `</div></nav>`;
  return html;
}

function buildRootPages({ courseHomeMd, syllabusMd, weekFiles }){
  const renderedHome = markdownToHtml(courseHomeMd);
  const homeTitle = `${COURSE_TITLE}`;
  const indexOut = path.join(ROOT, "index.html");
  const navData = buildNavStructure(weekFiles.map((wf) => wf.relPath));
  const navHtml = buildNavHtml({ fromOutputFile: indexOut, navData });
  const indexHtml = renderPage({
    fromOutputFile: indexOut,
    title: homeTitle,
    contentHtml: renderedHome,
    navHtml
  });
  fs.writeFileSync(indexOut, indexHtml, "utf-8");

  const renderedSyllabus = markdownToHtml(syllabusMd);
  const syllabusOut = path.join(ROOT, "syllabus.html");
  const navHtml2 = buildNavHtml({ fromOutputFile: syllabusOut, navData });
  const syllabusHtml = renderPage({
    fromOutputFile: syllabusOut,
    title: "Course Syllabus - " + COURSE_TITLE,
    contentHtml: renderedSyllabus,
    navHtml: navHtml2
  });
  fs.writeFileSync(syllabusOut, syllabusHtml, "utf-8");
}

async function main(){
  ensureDir(PAGES_DIR);
  const allMd = walkMarkdown(CONTENT_DIR);

  const courseHomePath = path.join(CONTENT_DIR, "course-home.md");
  const syllabusPath = path.join(CONTENT_DIR, "syllabus.md");

  if(!fs.existsSync(courseHomePath)){
    throw new Error("Missing content/course-home.md");
  }
  if(!fs.existsSync(syllabusPath)){
    throw new Error("Missing content/syllabus.md");
  }

  const courseHomeMd = fs.readFileSync(courseHomePath, "utf-8");
  const syllabusMd = fs.readFileSync(syllabusPath, "utf-8");

  // Week markdown: phase-* / module-* / week-*.md
  const weekFiles = [];
  const labFiles = [];
  for(const p of allMd){
    const rel = path.relative(CONTENT_DIR, p);
    const parts = rel.split(path.sep);
    if(parts.length !== 3) continue;
    if(!parts[0].startsWith("phase-")) continue;
    if(!parts[1].startsWith("module-")) continue;
    if(!/^week-\d+\.md$/.test(parts[2])) continue;
    weekFiles.push({ absPath: p, relPath: rel });
  }

  // Lab markdown: phase-* / module-* / labs / week-*.md
  for(const p of allMd){
    const rel = path.relative(CONTENT_DIR, p);
    const parts = rel.split(path.sep);
    if(parts.length !== 4) continue;
    if(!parts[0].startsWith("phase-")) continue;
    if(!parts[1].startsWith("module-")) continue;
    if(parts[2] !== "labs") continue;
    if(!/^week-\d+.*\.md$/.test(parts[3])) continue;
    labFiles.push({ absPath: p, relPath: rel });
  }

  if(weekFiles.length === 0){
    throw new Error("No week markdown found under content/phase-*/module-*/week-*.md");
  }

  // Generate week pages
  const navData = buildNavStructure(weekFiles.map((wf) => wf.relPath));

  for(const wf of weekFiles){
    const md = fs.readFileSync(wf.absPath, "utf-8");
    const heading = getFirstHeading(md);
    const pageTitle = heading ? `${heading} - ${COURSE_TITLE}` : COURSE_TITLE;
    const html = markdownToHtml(md);

    const outFile = markdownRelToOutput(wf.relPath);
    ensureDir(path.dirname(outFile));

    const navHtml = buildNavHtml({ fromOutputFile: outFile, navData });
    const pageHtml = renderPage({
      fromOutputFile: outFile,
      title: pageTitle,
      contentHtml: html,
      navHtml
    });
    fs.writeFileSync(outFile, pageHtml, "utf-8");
  }

  // Generate lab pages (not included in sidebar nav)
  for(const lf of labFiles){
    const md = fs.readFileSync(lf.absPath, "utf-8");
    const heading = getFirstHeading(md);
    const pageTitle = heading ? `${heading} - ${COURSE_TITLE}` : COURSE_TITLE;
    const html = markdownToHtml(md);

    const outFile = markdownRelToLabOutput(lf.relPath);
    ensureDir(path.dirname(outFile));

    const navHtml = buildNavHtml({ fromOutputFile: outFile, navData });
    const pageHtml = renderPage({
      fromOutputFile: outFile,
      title: pageTitle,
      contentHtml: html,
      navHtml
    });
    fs.writeFileSync(outFile, pageHtml, "utf-8");
  }

  // Generate root index and syllabus from markdown
  buildRootPages({ courseHomeMd, syllabusMd, weekFiles });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

