(function () {
  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  ready(function () {
    var form = document.getElementById("contact-form");
    if (!form) return;

    var config = window.SITE_CONFIG || { contact: {}, form: {} };
    var status = document.getElementById("form-status");
    var submit = form.querySelector("[type='submit']");
    var select = form.querySelector("[name='projectType']");

    function setService(value) {
      if (!select || !value) return;
      var match = Array.prototype.some.call(select.options, function (option) {
        return option.value === value;
      });
      if (!match) return;
      select.value = value;
      select.classList.add("is-prefilled");
      var field = select.closest(".field");
      if (field) field.classList.remove("is-invalid");
      window.setTimeout(function () { select.classList.remove("is-prefilled"); }, 1800);
    }

    var params = new URLSearchParams(window.location.search);
    if (params.get("service")) setService(params.get("service"));

    document.querySelectorAll("[data-service]").forEach(function (link) {
      link.addEventListener("click", function () {
        setService(link.getAttribute("data-service"));
      });
    });

    function fieldError(name, message) {
      var field = form.querySelector('[name="' + name + '"]');
      if (!field) return;
      var wrap = field.closest(".field") || field.closest("fieldset");
      if (!wrap) return;
      wrap.classList.add("is-invalid");
      var slot = wrap.querySelector(".field-error");
      if (slot) slot.textContent = message;
      field.setAttribute("aria-invalid", "true");
    }

    function clearErrors() {
      form.querySelectorAll(".is-invalid").forEach(function (node) { node.classList.remove("is-invalid"); });
      form.querySelectorAll(".field-error").forEach(function (node) { node.textContent = ""; });
      form.querySelectorAll("[aria-invalid]").forEach(function (node) { node.removeAttribute("aria-invalid"); });
    }

    function showStatus(kind, html) {
      if (!status) return;
      status.className = "form-status is-show " + (kind === "ok" ? "is-ok" : "is-err");
      status.innerHTML = html;
    }

    function data() {
      return {
        name: form.name.value.trim(),
        email: form.email.value.trim(),
        company: form.company.value.trim(),
        projectType: form.projectType.value,
        budget: form.budget.value,
        timeline: form.timeline.value,
        message: form.message.value.trim(),
        preferredContact: (form.querySelector("[name='preferredContact']:checked") || {}).value || "",
        _gotcha: form._gotcha ? form._gotcha.value : ""
      };
    }

    function mailto(payload) {
      var body = [
        "Name: " + payload.name,
        "Email: " + payload.email,
        "Company: " + (payload.company || "-"),
        "Project type: " + payload.projectType,
        "Budget: " + payload.budget,
        "Timeline: " + payload.timeline,
        "Preferred contact: " + payload.preferredContact,
        "",
        payload.message
      ].join("\n");
      return "mailto:" + config.contact.email + "?subject=" + encodeURIComponent("Project inquiry from " + payload.name) + "&body=" + encodeURIComponent(body);
    }

    function validate(payload) {
      clearErrors();
      var errors = [];
      if (payload.name.length < 2) errors.push(["name", "Enter your name."]);
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.email)) errors.push(["email", "Enter a valid email address."]);
      if (!payload.projectType) errors.push(["projectType", "Select a project type."]);
      if (!payload.budget) errors.push(["budget", "Select a budget range."]);
      if (!payload.timeline) errors.push(["timeline", "Select a timeline."]);
      if (payload.message.length < 20) errors.push(["message", "Describe the project in at least a sentence."]);
      if (!payload.preferredContact) errors.push(["preferredContact", "Choose how you prefer to be contacted."]);
      errors.forEach(function (item) { fieldError(item[0], item[1]); });
      if (errors.length) {
        var first = form.querySelector("[name='" + errors[0][0] + "']");
        if (first) first.focus();
        return false;
      }
      return true;
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var payload = data();
      if (!validate(payload)) return;

      if (payload._gotcha) {
        showStatus("ok", "<p>Message received.</p>");
        form.reset();
        return;
      }

      var endpoint = config.form && config.form.endpoint;
      var fallback = '<p><a href="' + mailto(payload) + '">Open this inquiry in your email app</a>.</p>';

      if (!endpoint) {
        showStatus("err", "<p>This form is not connected to an inbox yet. Email " + config.contact.email + " directly, or send the same details from your email app. Nothing was transmitted.</p>" + fallback);
        return;
      }

      if (submit) {
        submit.disabled = true;
        submit.setAttribute("aria-busy", "true");
        submit.dataset.label = submit.textContent;
        submit.textContent = "Sending…";
      }

      fetch(endpoint, {
        method: "POST",
        headers: { Accept: "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
          name: payload.name,
          email: payload.email,
          company: payload.company,
          projectType: payload.projectType,
          budget: payload.budget,
          timeline: payload.timeline,
          message: payload.message,
          preferredContact: payload.preferredContact,
          _subject: "Portfolio inquiry from " + payload.name,
          _gotcha: payload._gotcha
        })
      }).then(function (response) {
        if (!response.ok) throw new Error("Request failed");
        showStatus("ok", "<p>Message sent. Muhammad Saad will reply to the email you provided, or by the contact method you selected.</p>");
        form.reset();
      }).catch(function () {
        showStatus("err", "<p>The message could not be sent. Please use email or WhatsApp, or try again in a moment.</p>" + fallback);
      }).finally(function () {
        if (submit) {
          submit.disabled = false;
          submit.removeAttribute("aria-busy");
          submit.textContent = submit.dataset.label || "Send message";
        }
      });
    });
  });
})();
