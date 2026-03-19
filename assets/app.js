(function(){
  const root = document.documentElement;

  // Build a small "On this page" table of contents from h2 headings.
  // This keeps long weekly pages navigable without manual markup.
  const slugify = (s) => {
    const base = (s || "")
      .toLowerCase()
      .trim()
      // Keep Unicode letters/numbers so non-English headings produce stable ids.
      // Falls back to "section" when the result is empty.
      .replace(/[^\p{L}\p{N}]+/gu, "-")
      .replace(/(^-|-$)/g, "");
    return base || "section";
  };

  const buildToc = () => {
    const articles = document.querySelectorAll("article.prose");
    for(const article of articles){
      const headings = Array.from(article.querySelectorAll("h2"));
      if(headings.length === 0) continue;

      const existing = article.querySelector(".proseToc");
      if(existing) existing.remove();

      const nav = document.createElement("nav");
      nav.className = "proseToc";
      nav.setAttribute("aria-label", "On this page");

      const title = document.createElement("div");
      title.className = "proseTocTitle";
      title.textContent = "On this page";

      const list = document.createElement("div");
      list.className = "proseTocList";

      headings.forEach((h, idx) => {
        if(!h.id){
          h.id = `${slugify(h.textContent)}-${idx+1}`;
        }
        const link = document.createElement("a");
        link.className = "proseTocLink";
        link.href = `#${h.id}`;
        link.textContent = h.textContent;
        list.appendChild(link);
      });

      nav.appendChild(title);
      nav.appendChild(list);

      const h1 = article.querySelector("h1");
      if(h1 && h1.parentNode === article && h1.nextSibling){
        article.insertBefore(nav, h1.nextSibling);
      }else{
        article.prepend(nav);
      }
    }
  };

  try{
    buildToc();
  }catch(e){
    // Don't break page rendering if TOC generation fails.
    try{ console.debug("TOC build failed", e); }catch(_){}
  }

  // Accessibility: skip link (keyboard/screen-reader friendly).
  try{
    const main = document.querySelector("main.content");
    if(main && !main.id){
      main.id = "mainContent";
    }
    if(!document.getElementById("skipToContent")){
      const link = document.createElement("a");
      link.id = "skipToContent";
      link.className = "skipLink";
      link.href = "#mainContent";
      link.textContent = "Skip to content";
      document.body.insertBefore(link, document.body.firstChild);
    }
  }catch(e){
    try{ console.debug("Skip link setup failed", e); }catch(_){}
  }

  // Sidebar toggle for small screens
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebarNav = document.getElementById('siteNav');
  const isMobile = () => !!(window.matchMedia && window.matchMedia('(max-width: 980px)').matches);

  const syncSidebarA11y = () => {
    if(!sidebarToggle || !sidebarNav) return;
    const mobile = isMobile();
    const open = root.dataset.sidebarOpen === 'true';

    // On desktop the sidebar is always visible; on mobile we hide it via CSS.
    if(!mobile){
      sidebarToggle.setAttribute('aria-expanded', 'true');
      sidebarNav.setAttribute('aria-hidden', 'false');
      return;
    }

    sidebarToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    sidebarNav.setAttribute('aria-hidden', open ? 'false' : 'true');
  };

  if(sidebarToggle){
    sidebarToggle.addEventListener('click', () => {
      const next = root.dataset.sidebarOpen === 'true' ? 'false' : 'true';
      root.dataset.sidebarOpen = next;
      syncSidebarA11y();
    });
  }
  // Set initial aria state.
  try{ syncSidebarA11y(); }catch(e){ try{ console.debug("Sidebar a11y sync failed", e); }catch(_){}} 

  // Theme toggle (light/dark)
  const themeToggle = document.getElementById('themeToggle');
  const updateThemeButton = (theme) => {
    if(!themeToggle) return;
    const isLight = theme === 'light';
    themeToggle.setAttribute('aria-pressed', isLight ? 'true' : 'false');
    themeToggle.setAttribute('aria-label', isLight ? 'Switch to dark theme' : 'Switch to light theme');
    themeToggle.textContent = isLight ? 'Light' : 'Dark';
  };
  const applyTheme = (theme) => {
    if(theme === 'light'){
      root.dataset.theme = 'light';
    }else{
      delete root.dataset.theme;
    }
    updateThemeButton(theme);
    try{ localStorage.setItem('theme', theme); }catch(e){}
  };
  try{
    const saved = localStorage.getItem('theme');
    if(saved === 'light' || saved === 'dark'){
      applyTheme(saved === 'light' ? 'light' : 'dark');
    }else if(window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches){
      applyTheme('light');
    }
  }catch(e){
    try{ console.debug("Theme init failed", e); }catch(_){}
  }

  if(themeToggle){
    themeToggle.addEventListener('click', () => {
      const current = root.dataset.theme === 'light' ? 'light' : 'dark';
      applyTheme(current === 'light' ? 'dark' : 'light');
    });
  }

  // Active nav link highlighting
  const normalizePath = (p) => {
    // Normalize paths between directory-style links (".../week-1/") and direct index pages (".../week-1/index.html")
    let s = p || "";
    s = s.replace(/\/index\.html$/, "/");
    s = s.replace(/\/+$/, "/");
    return s;
  };

  const active = (a) => {
    try{
      const aUrl = new URL(a.getAttribute('href'), window.location.href);
      return normalizePath(aUrl.pathname) === normalizePath(window.location.pathname);
    }catch(e){
      return false;
    }
  };
  const links = document.querySelectorAll('[data-nav-link="true"]');
  for(const a of links){
    if(active(a)){
      a.classList.add('active');
      a.setAttribute('aria-current', 'page');
    }
  }
})();

