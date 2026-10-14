#!/usr/bin/env python3
"""Rebuilds everything derived from projects_data.py:
   assets/js/projects.js, projects/*.html case studies, the home-page no-JS list,
   sitemap.xml and every banner SVG.   Run from the project root:  python3 tools/build_site.py"""
import os, re, json, html, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from projects_data import PROJECTS
E = html.escape
DOMAIN = "https://muhammadsaad.dev"

# ---- keep the page chrome (header/footer) from an existing case page ----------
chrome_path = os.path.join(HERE, "page_chrome.json")
if not os.path.exists(chrome_path):
    t = open(os.path.join(ROOT, "projects", "ai-knowledge-assistant.html"), encoding="utf-8").read()
    json.dump({"top": t[t.index("<body>"):t.index('<main id="main">')], "bottom": t[t.index("</main>"):]}, open(chrome_path, "w", encoding="utf-8"))
CH = json.load(open(chrome_path, encoding="utf-8"))

def txt(p, key):  # legacy text is already HTML-safe, new text is plain
    v = p.get(key) or ""
    return v if not p["isnew"] else E(v)

def derive_arch(p):
    g = {"Interface": [], "API and logic": [], "Data": [], "Platform and services": []}
    for t in p["tech"]:
        l = t.lower()
        if any(k in l for k in ("sql", "cosmos", "mongo", "storage")): g["Data"].append(t)
        elif any(k in l for k in ("language", "hosted", "azure", "aws", "docker", "ci/cd", "queue", "email", "payment")): g["Platform and services"].append(t)
        elif any(k in l for k in ("angular", "web ui", "typescript", "javascript", "html", "css", "rxjs", "ngrx")): g["Interface"].append(t)
        else: g["API and logic"].append(t)
    return [(k, ", ".join(v)) for k, v in g.items() if v]

def case_page(i, p):
    prev, nxt = PROJECTS[i - 1], PROJECTS[(i + 1) % len(PROJECTS)]
    title = E(p["title"]); concept = p["status"] != "professional"
    desc = p["desc"] if not p["isnew"] else E(p["summary"])
    lede = p["lede"] if not p["isnew"] else E(f'{p["type"]}. {p["summary"]}')
    url = f'{DOMAIN}/projects/{p["id"]}.html'
    head = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Muhammad Saad</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#080920">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title} | Muhammad Saad">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOMAIN}/assets/images/og-share.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} | Muhammad Saad">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{DOMAIN}/assets/images/og-share.png">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../assets/css/styles.css">
  <script>
    (function () {{
      try {{
        var stored = localStorage.getItem("saad-theme");
        var theme = stored === "light" || stored === "dark" ? stored : "dark";
        document.documentElement.setAttribute("data-theme", theme);
      }} catch (error) {{
        document.documentElement.setAttribute("data-theme", "dark");
      }}
      if (location.protocol === "http:" || location.protocol === "https:") {{
        var manifestLink = document.createElement("link");
        manifestLink.rel = "manifest";
        manifestLink.href = "../site.webmanifest";
        document.head.appendChild(manifestLink);
      }}
      document.documentElement.classList.add("js");
    }})();
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{ "@type": "WebPage", "name": "{title}", "description": "{desc}", "url": "{url}", "author": {{ "@type": "Person", "name": "Muhammad Saad", "url": "{DOMAIN}/" }} }},
      {{ "@type": "BreadcrumbList", "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{DOMAIN}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Projects", "item": "{DOMAIN}/#projects" }},
        {{ "@type": "ListItem", "position": 3, "name": "{title}", "item": "{url}" }} ] }}
    ]
  }}
  </script>
</head>
'''
    stack = "".join(f"<li>{E(s)}</li>" for s in p["stack"])
    funcs = "".join(f"<li>{x if not p['isnew'] else E(x)}</li>" for x in (p["functionality"]))
    skills = "".join(f"<li>{E(s)}</li>" for s in p["skills"])
    arch = ""
    if concept:
        layers = p.get("arch") or derive_arch(p)
        lis = "".join(f'<li><span class="arch__tag">{E(a)}</span><span>{E(b)}</span></li>' for a, b in layers)
        arch = f'''<section class="case-block case-block--wide"><h2>Proposed architecture</h2><p class="arch-note">How this concept would be built. It is a design sketch, not a description of a live system.</p><ol class="arch">{lis}</ol></section>
      '''
    status = p["outcome"] or "This is a concept project. It describes a product Muhammad Saad can design and build. It is not a completed client engagement, and it does not represent a live system or a measured business result."
    status_h = "Status" if concept else "Outcome"
    value_label = "Value this kind of system is built to deliver" if concept else "Value delivered"
    tech_h = "Suggested technologies" if concept else "Technical focus"
    body = f'''<main id="main">
    <article class="wrap case">
      <header class="page-intro">
        <p class="crumbs"><a href="../index.html#home">Home</a> / <a href="../index.html#projects">Projects</a> / {title}</p>
        <p class="badge-row"><span class="badge badge--{p['status']}">{E(p['statusLabel'])}</span><span class="badge">{E(p['label'])}</span></p>
        <h1>{title}</h1>
        <p class="lede">{lede}</p>
      </header>
      <div id="case-visual" data-project-id="{p['id']}"></div>
      <div class="case-grid">
        <section class="case-block"><h2>The problem</h2><p>{txt(p,'need')}</p></section>
        <section class="case-block"><h2>The solution</h2><p>{txt(p,'approach')}</p></section>
        <section class="case-block"><h2>Key features</h2><ul>{funcs}</ul></section>
        <section class="case-block case-block--value"><h2>{value_label}</h2><p>{E(p['value'])}</p><h3>Strengths this project shows</h3><ul class="pills">{skills}</ul></section>
      </div>
      {arch}<section class="case-block" style="margin-top:1rem"><h2>{status_h}</h2><p>{status}</p></section>
      <div class="cta-band">
        <div>
          <h2>Discuss a project in this area</h2>
          <p>Share the context, the constraint, and whether you need a new build or help inside an existing codebase.</p>
        </div>
        <a class="btn btn-primary" href="../index.html?service={p['service']}#contact">Get a Free Quote</a>
      </div>
      <nav class="pager" aria-label="Other projects"><a class="text-link" href="{prev['id']}.html">Previous: {E(prev['title'])}</a><a class="text-link" href="{nxt['id']}.html">Next: {E(nxt['title'])}</a></nav>
    </article>
  </main>
  '''
    return head + CH["top"] + body + CH["bottom"].lstrip("\n").replace("</main>\n", "", 1) if False else head + CH["top"] + body + CH["bottom"].split("</main>", 1)[1].lstrip("\n")

# ---- pages ------------------------------------------------------------------
for i, p in enumerate(PROJECTS):
    open(os.path.join(ROOT, "projects", p["id"] + ".html"), "w", encoding="utf-8").write(case_page(i, p))

# ---- projects.js ------------------------------------------------------------
fields = ["id", "title", "type", "summary", "status", "statusLabel", "label", "categories", "stack", "features", "value", "page", "layout", "mockTitle", "accent"]
data = [{k: p[k] for k in fields} for p in PROJECTS]
js = '''(function () {
  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (char) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char];
    });
  }

  // GENERATED by tools/build_site.py from tools/projects_data.py. Edit the data file, not this one.
  // Banner art: assets/images/projects/<id>.svg (cards) and <id>-wide.svg (case pages).
  function assetBase() {
    return /\\/projects\\//.test(window.location.pathname) ? "../" : "";
  }

  window.renderProjectMock = function (project, large) {
    var src = assetBase() + "assets/images/projects/" + project.id + (large ? "-wide" : "") + ".svg";
    if (large) {
      return (
        '<figure class="case-banner"><img src="' + src + '" width="1600" height="640" alt="Illustrative banner for ' +
        escapeHtml(project.title) + '. Illustrative interface with demo data, not a screenshot of a client system."><figcaption>Illustrative interface preview with demo data. Not a screenshot of a client system.</figcaption></figure>'
      );
    }
    return '<img src="' + src + '" width="800" height="500" loading="lazy" alt="">';
  };

  window.PORTFOLIO = ''' + json.dumps(data, indent=2, ensure_ascii=False) + ''';

  window.PORTFOLIO.forEach(function (project) {
    project.pageFromRoot = project.page;
  });

  var grid = document.getElementById("project-grid");
  if (!grid) return;

  var prefix = grid.getAttribute("data-prefix") || "";
  grid.innerHTML = window.PORTFOLIO.map(function (project) {
    var href = prefix + project.page;
    return (
      '<article class="project-card" data-status="' + project.status + '" data-categories="' + project.categories.join(" ") + '">' +
      '<div class="project-card__media">' + window.renderProjectMock(project, false) +
      '<p class="badge badge--' + project.status + '">' + escapeHtml(project.statusLabel) + "</p>" +
      '<p class="project-card__label">' + escapeHtml(project.label) + "</p></div>" +
      '<div class="project-card__body">' +
      '<p class="project-card__type">' + escapeHtml(project.type) + "</p>" +
      '<h3><a href="' + href + '">' + escapeHtml(project.title) + "</a></h3>" +
      "<p>" + escapeHtml(project.summary) + "</p>" +
      '<ul class="project-card__features">' + project.features.map(function (item) { return "<li>" + escapeHtml(item) + "</li>"; }).join("") + "</ul>" +
      '<p class="project-card__value"><strong>Value</strong> ' + escapeHtml(project.value) + "</p>" +
      '<a class="text-link" href="' + href + '">View case study</a>' +
      "</div></article>"
    );
  }).join("");
})();
'''
open(os.path.join(ROOT, "assets/js/projects.js"), "w", encoding="utf-8").write(js)

# ---- index.html: no-JS list, filter chip, AI stack card ---------------------
ip = os.path.join(ROOT, "index.html"); s = open(ip, encoding="utf-8").read()
li = "\n".join(f'            <li><a href="projects/{p["id"]}.html">{E(p["title"])}</a></li>' for p in PROJECTS)
s = re.sub(r'(<p>Project pages are available without JavaScript:</p>\s*<ul>\n).*?(\n          </ul>)', lambda m: m[1] + li + m[2], s, flags=re.S)
if 'data-filter="remote"' not in s:
    s = s.replace('<button class="chip" type="button" data-filter="automation"', '<button class="chip" type="button" data-filter="remote" aria-pressed="false">Remote and International</button>\n            <button class="chip" type="button" data-filter="automation"', 1)
if "AI integration</h3>" not in s:
    s = s.replace('</article>\n        </div>\n      </div>\n    </section>\n\n    <section class="banner-strip"', '</article>\n          <article class="stack-card"><h3>AI integration</h3><ul><li>Hosted language-model APIs</li><li>Question answering over documents</li><li>Prompt and context design</li><li>Human-review workflows</li><li>Summaries and classification</li></ul></article>\n        </div>\n      </div>\n    </section>\n\n    <section class="banner-strip"', 1)
open(ip, "w", encoding="utf-8").write(s)

# ---- sitemap -----------------------------------------------------------------
sp = os.path.join(ROOT, "sitemap.xml"); sm = open(sp, encoding="utf-8").read()
for p in PROJECTS:
    loc = f'{DOMAIN}/projects/{p["id"]}.html'
    if loc not in sm:
        sm = sm.replace("</urlset>", f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-10-14</lastmod>\n    <priority>0.6</priority>\n  </url>\n</urlset>')
open(sp, "w", encoding="utf-8").write(sm)

subprocess.check_call([sys.executable, os.path.join(HERE, "make_banners.py")])
print("built", len(PROJECTS), "projects")
