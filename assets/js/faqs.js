(function () {
  window.FAQS = [
    {
      q: "What kinds of projects do you take on?",
      a: "Custom web applications, ASP.NET Core APIs, Angular front ends, SQL Server work, authentication, cloud deployment, and improvements to an existing .NET or Angular codebase. A good fit is a business system that needs a senior engineer who can own the technical path from discussion to release."
    },
    {
      q: "Do you work in stacks other than .NET and Angular?",
      a: "Yes. C#, ASP.NET Core, Angular, and SQL Server are where my experience runs deepest, and that is where I would normally recommend starting. If your product already runs on another stack, such as Node.js, Python, Java, PHP, React, or Vue, I am open to building in it. We agree scope after a short technical conversation, and I will say plainly if a specialist in that stack would serve you better."
    },
    {
      q: "How much does a project cost, and how long does it take?",
      a: "Both depend on scope, integrations, and how finished the requirements are. A focused internal tool is a different engagement from a multi-module business system. After a short discovery conversation you receive a written estimate before any build starts. Published rates stay hidden until they are finalized in the site configuration."
    },
    {
      q: "Can you join an existing development team?",
      a: "Yes. Agencies and in-house teams can bring Muhammad Saad in for ASP.NET Core, Angular, database, or delivery support alongside people who already know the product."
    },
    {
      q: "How do communication and progress updates work?",
      a: "You choose a primary channel — email, WhatsApp, or scheduled calls — and receive progress in plain language, including what shipped, what is blocked, and what comes next. Technical detail is available when you want it, without making it the only way to follow the work."
    },
    {
      q: "Will you sign an NDA?",
      a: "Yes. A reasonable non-disclosure agreement can be signed before architecture, data, or commercial details are discussed."
    },
    {
      q: "Do you offer support after launch?",
      a: "Yes. Launch can include a handover and an agreed support window. Ongoing maintenance is available as a monthly retainer or as scheduled fixes and improvements."
    },
    {
      q: "Who owns the source code?",
      a: "On client projects, the source code is delivered to you under the terms agreed in writing before work starts. Ownership and repository access are part of that agreement, not an afterthought at the end."
    },
    {
      q: "Can you work across time zones?",
      a: "Muhammad Saad is based in Riyadh, Saudi Arabia (Arabia Standard Time, UTC+3) and works remotely with clients in the GCC and internationally. Overlapping hours are agreed up front so reviews and questions have a predictable window."
    }
  ];

  var root = document.getElementById("faq-list");
  if (!root) return;

  root.innerHTML = window.FAQS.map(function (item, index) {
    var panelId = "faq-panel-" + index;
    var buttonId = "faq-button-" + index;
    return (
      '<article class="faq-item">' +
      "<h3><button type=\"button\" id=\"" + buttonId + "\" aria-expanded=\"false\" aria-controls=\"" + panelId + "\">" + item.q + "</button></h3>" +
      '<div class="faq-panel" id="' + panelId + '" role="region" aria-labelledby="' + buttonId + '" hidden><p>' + item.a + "</p></div>" +
      "</article>"
    );
  }).join("");

  var schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: window.FAQS.map(function (item) {
      return {
        "@type": "Question",
        name: item.q,
        acceptedAnswer: { "@type": "Answer", text: item.a }
      };
    })
  };
  var script = document.createElement("script");
  script.type = "application/ld+json";
  script.textContent = JSON.stringify(schema);
  document.head.appendChild(script);
})();
