(function () {
  function icon(path) {
    return '<svg viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' + path + "</svg>";
  }

  var icons = {
    app: icon('<rect x="4" y="6" width="24" height="18" rx="2"/><path d="M4 11h24M9 24v3h14v-3"/>'),
    api: icon('<path d="M7 9l-4 7 4 7M25 9l4 7-4 7M13 25l6-18"/>'),
    ui: icon('<rect x="4" y="5" width="11" height="9" rx="1.5"/><rect x="17" y="5" width="11" height="14" rx="1.5"/><rect x="4" y="16" width="11" height="11" rx="1.5"/>'),
    db: icon('<ellipse cx="16" cy="8" rx="8" ry="3"/><path d="M8 8v10c0 1.7 3.6 3 8 3s8-1.3 8-3V8"/><path d="M8 13c0 1.7 3.6 3 8 3s8-1.3 8-3"/>'),
    cloud: icon('<path d="M10 23h12a5 5 0 0 0 .4-10 7 7 0 0 0-13.2 2A4.5 4.5 0 0 0 10 23z"/><path d="M16 19v6M13.5 22.5 16 25l2.5-2.5"/>'),
    shield: icon('<path d="M16 4l9 4v7c0 6-3.8 9.8-9 11-5.2-1.2-9-5-9-11V8l9-4z"/><path d="M12 16l2.6 2.6L20.5 13"/>'),
    review: icon('<path d="M8 6h12l4 4v16H8z"/><path d="M20 6v4h4M11 16h8M11 20h6"/>')
  };

  window.SERVICES = [
    {
      title: "Custom Web Application Development",
      benefit: "A product shaped around the way your business actually works.",
      text: "Purpose-built web applications for operations, customers, and internal teams, structured so the next feature does not force a rewrite.",
      icon: icons.app
    },
    {
      title: "ASP.NET Core API and Backend Development",
      benefit: "A reliable core for web, mobile, and partner integrations.",
      text: "Secure Web APIs with validation, clear boundaries, and data access that can carry real business rules.",
      icon: icons.api
    },
    {
      title: "Angular Frontend Development",
      benefit: "Interfaces people can use without a training manual.",
      text: "Typed Angular applications with predictable structure and screens that stay responsive as the product grows.",
      icon: icons.ui
    },
    {
      title: "SQL Server and Database Optimization",
      benefit: "Data the application can trust under real usage.",
      text: "Schema design, querying, and performance work for SQL Server, plus practical use of other databases when the product needs them.",
      icon: icons.db
    },
    {
      title: "Cloud Deployment and DevOps",
      benefit: "Releases that do not depend on one person's laptop.",
      text: "Environments, pipelines, and hosting on Azure or AWS so the software can be shipped and updated with less risk.",
      icon: icons.cloud
    },
    {
      title: "Authentication and Application Security",
      benefit: "Access control that matches how your organization works.",
      text: "Sign-in, authorization, and identity-aware workflows for applications that handle sensitive business data.",
      icon: icons.shield
    },
    {
      title: "Technical Consulting, Code Review, and Maintenance",
      benefit: "A senior engineer who can join, assess, and improve what you already have.",
      text: "Architecture advice, code review, bug fixing, and planned maintenance for teams that need depth without hiring a department.",
      icon: icons.review
    }
  ];

  var root = document.getElementById("service-grid");
  if (!root) return;

  root.innerHTML = window.SERVICES.map(function (service) {
    return (
      '<article class="service-card">' +
      '<div class="service-card__icon">' + service.icon + "</div>" +
      "<h3>" + service.title + "</h3>" +
      '<p class="service-card__benefit">' + service.benefit + "</p>" +
      "<p>" + service.text + "</p>" +
      '<a class="text-link" href="#contact" data-service="' + service.title.replace(/"/g, "&quot;") + '">Discuss this service</a>' +
      "</article>"
    );
  }).join("");
})();
