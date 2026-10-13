(function () {
  window.EXPERIENCE = [
    {
      org: "Euphoria XR",
      role: "Senior Software Engineer / Technical Lead",
      dates: "2024–2026",
      summary: "Senior full-stack engineering with technical leadership on web products, from implementation through delivery coordination. Specific achievements are added only when they are confirmed for publication."
    },
    {
      org: "ArhamSoft",
      role: "Full-stack software development",
      dates: "2022–2023",
      summary: "Web application development during this part of Muhammad Saad's full-stack career. An official job title can replace this line when it is confirmed."
    },
    {
      org: "Vision Plus Solution",
      role: "Full-stack software development",
      dates: "2021–2022",
      summary: "Software development on business web applications. An official job title can replace this line when it is confirmed."
    },
    {
      org: "AlphaCore Technology",
      role: "Full-stack software development",
      dates: "2020–2021",
      summary: "Early professional software development in the same full-stack practice. An official job title can replace this line when it is confirmed."
    }
  ];

  var root = document.getElementById("timeline");
  if (!root) return;

  root.innerHTML = window.EXPERIENCE.map(function (item) {
    return (
      "<li>" +
      '<p class="dates">' + item.dates + "</p>" +
      "<h3>" + item.org + "</h3>" +
      '<p class="role">' + item.role + "</p>" +
      "<p>" + item.summary + "</p>" +
      "</li>"
    );
  }).join("");
})();
