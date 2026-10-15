(function () {
  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  ready(function () {
    var header = document.querySelector(".site-header");
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");
    var yearNodes = document.querySelectorAll("[data-year]");
    yearNodes.forEach(function (node) {
      node.textContent = String(new Date().getFullYear());
    });

    var config = window.SITE_CONFIG || {};
    document.querySelectorAll("[data-price]").forEach(function (node) {
      var key = node.getAttribute("data-price");
      var raw = config.pricing && config.pricing.models ? config.pricing.models[key] : "";
      var unpublished = !config.pricing || config.pricing.showRates === false || !raw || /^\[Add /.test(raw);
      node.textContent = unpublished ? "Rate available on request" : raw;
    });

    var githubSlot = document.getElementById("github-slot");
    var github = config.contact && config.contact.github;
    if (githubSlot && github && /^https?:\/\//.test(github)) {
      githubSlot.innerHTML = "";
      var link = document.createElement("a");
      link.href = github;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = "GitHub";
      githubSlot.appendChild(link);
    }


    if (toggle && nav && header) {
      var label = toggle.querySelector(".sr-only");
      function closeMenu() {
        header.classList.remove("is-open");
        document.body.classList.remove("nav-lock");
        toggle.setAttribute("aria-expanded", "false");
        if (label) label.textContent = "Open menu";
      }
      function openMenu() {
        header.classList.add("is-open");
        document.body.classList.add("nav-lock");
        toggle.setAttribute("aria-expanded", "true");
        if (label) label.textContent = "Close menu";
        var first = nav.querySelector("a");
        if (first) first.focus();
      }
      toggle.addEventListener("click", function () {
        if (header.classList.contains("is-open")) closeMenu();
        else openMenu();
      });
      nav.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", closeMenu);
      });
      document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") closeMenu();
      });
      window.addEventListener("resize", function () {
        if (window.innerWidth > 1080) closeMenu();
      });
    }

    var links = Array.prototype.slice.call(document.querySelectorAll('.site-nav a[href^="#"]'));
    var sections = links.map(function (link) {
      return document.querySelector(link.getAttribute("href"));
    }).filter(Boolean);

    var sliderMode = document.documentElement.classList.contains("slider-on");
    if (!sliderMode && links.length && sections.length && "IntersectionObserver" in window) {
      var active = null;
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          active = entry.target.id;
        });
        links.forEach(function (link) {
          var on = link.getAttribute("href") === "#" + active;
          if (on) link.setAttribute("aria-current", "true");
          else link.removeAttribute("aria-current");
        });
      }, { rootMargin: "-45% 0px -50% 0px", threshold: 0.01 });
      sections.forEach(function (section) { observer.observe(section); });
    }

    document.querySelectorAll(".faq-item button").forEach(function (button) {
      button.addEventListener("click", function () {
        var panel = document.getElementById(button.getAttribute("aria-controls"));
        var open = button.getAttribute("aria-expanded") === "true";
        button.setAttribute("aria-expanded", open ? "false" : "true");
        if (panel) panel.hidden = open;
      });
    });

    var category = "all";
    var status = "all";
    var cards = Array.prototype.slice.call(document.querySelectorAll(".project-card"));
    var live = document.getElementById("project-live");
    var empty = document.getElementById("project-empty");

    function applyFilters() {
      var visible = 0;
      cards.forEach(function (card) {
        var categories = (card.getAttribute("data-categories") || "").split(" ");
        var cardStatus = card.getAttribute("data-status");
        var show = (category === "all" || categories.indexOf(category) !== -1) && (status === "all" || cardStatus === status);
        card.hidden = !show;
        if (show) visible += 1;
      });
      if (live) {
        live.textContent = "Showing " + visible + (visible === 1 ? " project" : " projects");
      }
      if (empty) empty.hidden = visible !== 0;
    }

    document.querySelectorAll("[data-filter]").forEach(function (button) {
      button.addEventListener("click", function () {
        category = button.getAttribute("data-filter");
        document.querySelectorAll("[data-filter]").forEach(function (peer) {
          var on = peer === button;
          peer.classList.toggle("is-active", on);
          peer.setAttribute("aria-pressed", on ? "true" : "false");
        });
        applyFilters();
      });
    });

    document.querySelectorAll("[data-status-filter]").forEach(function (button) {
      button.addEventListener("click", function () {
        status = button.getAttribute("data-status-filter");
        document.querySelectorAll("[data-status-filter]").forEach(function (peer) {
          var on = peer === button;
          peer.classList.toggle("is-active", on);
          peer.setAttribute("aria-pressed", on ? "true" : "false");
        });
        applyFilters();
      });
    });

    if (cards.length) applyFilters();

    var reveals = document.querySelectorAll(".reveal");
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (sliderMode || reduce || !("IntersectionObserver" in window)) {
      reveals.forEach(function (node) { node.classList.add("is-in"); });
    } else {
      var revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0, rootMargin: "0px 0px -6% 0px" });
      reveals.forEach(function (node) { revealObserver.observe(node); });
    }

    var toTop = document.querySelector(".to-top");
    if (toTop && !sliderMode) {
      var onScroll = function () {
        toTop.hidden = window.scrollY < 500;
      };
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }

    var visual = document.getElementById("case-visual");
    if (visual && window.PORTFOLIO && window.renderProjectMock) {
      var project = window.PORTFOLIO.find(function (item) {
        return item.id === visual.getAttribute("data-project-id");
      });
      if (project) visual.innerHTML = window.renderProjectMock(project, true);
    }
  });
})();
