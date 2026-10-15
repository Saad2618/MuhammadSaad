/* Horizontal section slider.
   Turns the home page into a row of full-screen slides that move left and right,
   like swiping between screens on a phone. Everything still works as a normal
   long page if this script cannot run (the "slider-on" class is only styling). */
(function () {
  var root = document.documentElement;
  if (!root.classList.contains("slider-on")) return;

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  var TITLES = {
    home: "Home", services: "Services", why: "Why me", projects: "Projects", stack: "Core stack",
    "any-stack": "Any stack", tagline: "Built to last", about: "About", process: "Process",
    global: "Worldwide", pricing: "Pricing", faq: "FAQ", start: "Let\u2019s talk", contact: "Contact"
  };

  ready(function () {
    var main = document.getElementById("main");
    if (!main) { root.classList.remove("slider-on"); return; }
    var sections = Array.prototype.filter.call(main.children, function (el) { return el.tagName === "SECTION"; });
    if (sections.length < 2) { root.classList.remove("slider-on"); return; }

    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var deck = document.createElement("div");
    deck.id = "deck";
    var panels = sections.map(function (section, i) {
      var panel = document.createElement("div");
      var inner = document.createElement("div");
      var id = section.id || "slide-" + i;
      panel.className = "panel";
      panel.setAttribute("data-id", id);
      panel.setAttribute("role", "group");
      panel.setAttribute("aria-roledescription", "slide");
      panel.setAttribute("aria-label", (TITLES[id] || id) + ", " + (i + 1) + " of " + sections.length);
      panel.tabIndex = -1;
      inner.className = "panel__inner";
      inner.appendChild(section);
      panel.appendChild(inner);
      deck.appendChild(panel);
      return panel;
    });
    var footer = document.querySelector(".site-footer");
    if (footer) panels[panels.length - 1].querySelector(".panel__inner").appendChild(footer);
    main.appendChild(deck);

    var last = panels.length - 1;
    var index = 0;
    var navLinks = Array.prototype.slice.call(document.querySelectorAll('.site-nav a[href^="#"]'));

    /* ---- controls: previous, dots, next, label, progress ---- */
    var bar = document.createElement("nav");
    bar.className = "deck-bar";
    bar.setAttribute("aria-label", "Sections");
    var prev = document.createElement("button");
    prev.type = "button"; prev.className = "deck-btn"; prev.setAttribute("aria-label", "Previous section");
    prev.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    var next = document.createElement("button");
    next.type = "button"; next.className = "deck-btn"; next.setAttribute("aria-label", "Next section");
    next.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    var label = document.createElement("span");
    label.className = "deck-label";
    var dots = document.createElement("span");
    dots.className = "deck-dots";
    var dotEls = panels.map(function (panel, i) {
      var d = document.createElement("button");
      d.type = "button"; d.className = "deck-dot";
      d.setAttribute("aria-label", (TITLES[panel.getAttribute("data-id")] || "Section " + (i + 1)));
      d.title = d.getAttribute("aria-label");
      d.addEventListener("click", function () { go(i, { push: true }); });
      dots.appendChild(d);
      return d;
    });
    bar.appendChild(prev); bar.appendChild(label); bar.appendChild(dots); bar.appendChild(next);
    var progress = document.createElement("div");
    progress.className = "deck-progress";
    progress.innerHTML = "<span></span>";
    var live = document.createElement("p");
    live.className = "sr-only"; live.setAttribute("aria-live", "polite");
    document.body.appendChild(bar); document.body.appendChild(progress); document.body.appendChild(live);
    prev.addEventListener("click", function () { go(index - 1, { push: true }); });
    next.addEventListener("click", function () { go(index + 1, { push: true }); });

    /* ---- helpers ---- */
    function setTransform(extraPx) {
      deck.style.transform = "translate3d(calc(" + (-index * 100) + "% + " + (extraPx || 0) + "px),0,0)";
    }
    function titleOf(i) { return TITLES[panels[i].getAttribute("data-id")] || ""; }

    function indexFromId(id) {
      if (!id) return -1;
      var el = document.getElementById(id);
      var panel = el && el.closest ? el.closest(".panel") : null;
      return panel ? panels.indexOf(panel) : -1;
    }

    function update() {
      panels.forEach(function (panel, i) {
        var on = i === index;
        panel.classList.toggle("is-active", on);
        panel.classList.toggle("is-near", Math.abs(i - index) === 1);
        if (on) { panel.removeAttribute("inert"); panel.removeAttribute("aria-hidden"); }
        else { panel.setAttribute("inert", ""); panel.setAttribute("aria-hidden", "true"); }
        dotEls[i].classList.toggle("is-on", on);
        if (on) dotEls[i].setAttribute("aria-current", "true"); else dotEls[i].removeAttribute("aria-current");
      });
      prev.disabled = index === 0;
      next.disabled = index === last;
      label.textContent = titleOf(index);
      progress.firstChild.style.transform = "scaleX(" + ((index + 1) / panels.length) + ")";
      live.textContent = titleOf(index) + ", section " + (index + 1) + " of " + panels.length;
      var currentId = panels[index].getAttribute("data-id");
      navLinks.forEach(function (link) {
        if (link.getAttribute("href") === "#" + currentId) link.setAttribute("aria-current", "true");
        else link.removeAttribute("aria-current");
      });
    }

    var enterTimer = null;
    function go(target, opts) {
      opts = opts || {};
      target = Math.max(0, Math.min(last, target));
      var from = index;
      var dir = target >= from ? 1 : -1;
      index = target;
      var distance = Math.abs(target - from);
      deck.classList.remove("is-dragging");
      deck.style.transitionDuration = (opts.instant || reduce) ? "0s" : Math.min(0.62 + 0.07 * distance, 1.05) + "s";
      setTransform(0);
      update();
      var panel = panels[index];
      panel.scrollTop = 0;
      if (!opts.instant && !reduce && target !== from) {
        panel.style.setProperty("--dir", String(dir));
        panel.classList.add("is-entering");
        clearTimeout(enterTimer);
        enterTimer = setTimeout(function () { panel.classList.remove("is-entering"); }, 1300);
      }
      if (opts.push) {
        var id = panel.getAttribute("data-id");
        if (location.hash !== "#" + id) {
          try { history.pushState({ slide: index }, "", "#" + id); } catch (e) { /* file:// in some browsers */ }
        }
      }
      if (opts.focus !== false && !opts.instant) { try { panel.focus({ preventScroll: true }); } catch (e) {} }
    }

    /* ---- clicks on any in-page link become slides ---- */
    document.addEventListener("click", function (event) {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey) return;
      var link = event.target.closest && event.target.closest('a[href^="#"]');
      if (!link) return;
      var hash = link.getAttribute("href");
      if (hash === "#" || hash === "#top" || hash === "#home") { event.preventDefault(); go(0, { push: true }); return; }
      var i = indexFromId(hash.slice(1));
      if (i < 0) return;
      event.preventDefault();
      go(i, { push: true });
    });

    function fromHash(instant) {
      var i = indexFromId(decodeURIComponent((location.hash || "").slice(1)));
      go(i < 0 ? 0 : i, { instant: instant, focus: false });
    }
    window.addEventListener("popstate", function () { fromHash(false); });
    window.addEventListener("hashchange", function () { fromHash(false); });

    /* ---- find a scrollable row (like the project carousel) that can still move ---- */
    function rowThatCanScroll(el, dx) {
      while (el && el !== deck) {
        if (el.nodeType === 1) {
          var cs = getComputedStyle(el);
          if ((cs.overflowX === "auto" || cs.overflowX === "scroll") && el.scrollWidth > el.clientWidth + 2) {
            var max = el.scrollWidth - el.clientWidth;
            if (dx < 0 && el.scrollLeft < max - 2) return el;
            if (dx > 0 && el.scrollLeft > 2) return el;
          }
          if (el.tagName === "TEXTAREA" || el.tagName === "INPUT" && el.type === "range") return el;
        }
        el = el.parentNode;
      }
      return null;
    }

    /* ---- keyboard: left and right arrows ---- */
    document.addEventListener("keydown", function (event) {
      if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
      var t = event.target;
      if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
      var step = event.key === "ArrowRight" ? 1 : -1;
      var row = panels[index].querySelector(".project-grid, .service-grid");
      if (row && row.offsetParent && rowThatCanScroll(row.firstElementChild || row, -step)) {
        event.preventDefault();
        row.scrollBy({ left: step * Math.min(row.clientWidth * 0.85, 420), behavior: reduce ? "auto" : "smooth" });
        return;
      }
      event.preventDefault();
      go(index + step, { push: true });
    });

    /* ---- trackpad or mouse sideways scroll ---- */
    var wheelLock = 0, wheelSum = 0, wheelTimer = null;
    deck.addEventListener("wheel", function (event) {
      if (Math.abs(event.deltaX) < Math.abs(event.deltaY) * 1.2 || Math.abs(event.deltaX) < 4) return;
      if (rowThatCanScroll(event.target, event.deltaX > 0 ? -1 : 1)) return;
      var now = Date.now();
      if (now < wheelLock) return;
      wheelSum += event.deltaX;
      clearTimeout(wheelTimer);
      wheelTimer = setTimeout(function () { wheelSum = 0; }, 160);
      if (Math.abs(wheelSum) > 70) {
        go(index + (wheelSum > 0 ? 1 : -1), { push: true });
        wheelSum = 0; wheelLock = now + 850;
      }
    }, { passive: true });

    /* ---- touch and pen: drag the slides with your finger ---- */
    var drag = null;
    deck.addEventListener("pointerdown", function (event) {
      if (event.pointerType === "mouse") return;
      drag = { id: event.pointerId, x: event.clientX, y: event.clientY, t: Date.now(), mode: null, dx: 0, target: event.target };
    });
    deck.addEventListener("pointermove", function (event) {
      if (!drag || event.pointerId !== drag.id) return;
      var dx = event.clientX - drag.x, dy = event.clientY - drag.y;
      if (!drag.mode) {
        if (Math.abs(dx) > 10 && Math.abs(dx) > Math.abs(dy) * 1.25) {
          if (rowThatCanScroll(drag.target, dx)) { drag = null; return; }
          drag.mode = "h";
          deck.classList.add("is-dragging");
          try { deck.setPointerCapture(event.pointerId); } catch (e) {}
        } else if (Math.abs(dy) > 10) { drag = null; return; }
        else return;
      }
      drag.dx = dx;
      var off = dx;
      if ((index === 0 && dx > 0) || (index === last && dx < 0)) off = dx * 0.28;
      setTransform(off);
    });
    function endDrag(event) {
      if (!drag || event.pointerId !== drag.id) return;
      var d = drag; drag = null;
      if (d.mode !== "h") return;
      deck.classList.remove("is-dragging");
      var w = deck.clientWidth || window.innerWidth;
      var v = d.dx / Math.max(1, Date.now() - d.t);
      if (d.dx < -w * 0.16 || v < -0.45) go(index + 1, { push: true, focus: false });
      else if (d.dx > w * 0.16 || v > 0.45) go(index - 1, { push: true, focus: false });
      else go(index, { focus: false });
    }
    deck.addEventListener("pointerup", endDrag);
    deck.addEventListener("pointercancel", endDrag);

    /* ---- carousel buttons for the sideways rows (projects and services) ---- */
    var ARROW_L = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    var ARROW_R = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    function makeCarousel(grid, anchor, what) {
      if (!grid || !anchor || !anchor.parentNode) return;
      var controls = document.createElement("div");
      controls.className = "carousel-controls";
      controls.innerHTML = '<button type="button" class="deck-btn" data-dir="-1" aria-label="Scroll ' + what + ' left">' + ARROW_L + '</button><button type="button" class="deck-btn" data-dir="1" aria-label="Scroll ' + what + ' right">' + ARROW_R + '</button>';
      anchor.parentNode.insertBefore(controls, anchor.nextSibling);
      controls.addEventListener("click", function (event) {
        var b = event.target.closest("button"); if (!b) return;
        grid.scrollBy({ left: Number(b.getAttribute("data-dir")) * Math.min(grid.clientWidth * 0.85, 760), behavior: reduce ? "auto" : "smooth" });
      });
      var sync = function () {
        var max = grid.scrollWidth - grid.clientWidth;
        controls.children[0].disabled = grid.scrollLeft < 4;
        controls.children[1].disabled = grid.scrollLeft > max - 4;
      };
      grid.addEventListener("scroll", sync, { passive: true });
      window.addEventListener("resize", sync);
      document.addEventListener("click", function () { setTimeout(sync, 60); });
      sync();
    }
    makeCarousel(document.getElementById("project-grid"), document.getElementById("project-live"), "projects");
    makeCarousel(document.getElementById("service-grid"), document.querySelector("#services .section-head"), "services");

    root.classList.add("slider-ready");
    if (reduce) root.classList.add("slider-reduce");
    fromHash(true);
  });
})();
