(function () {
  "use strict";

  var SOURCE_URL =
    "https://d1p18nmj81zs72.cloudfront.net/klcnodes/klcnodes.html";

  var HEADINGS = {
    direct: "KLC Direct Access Resource Availability",
    slurm: "KLC Slurm Node Availability",
  };

  function normalizeText(text) {
    return text.replace(/\s+/g, " ").trim();
  }

  function findTableAfterHeading(doc, headingText) {
    var headings = doc.querySelectorAll("h2");

    for (var i = 0; i < headings.length; i += 1) {
      if (normalizeText(headings[i].textContent) !== headingText) {
        continue;
      }

      var sibling = headings[i].nextElementSibling;
      while (sibling) {
        if (sibling.tagName === "TABLE") {
          return sibling;
        }
        sibling = sibling.nextElementSibling;
      }
    }

    return null;
  }

  function styleTable(table) {
    table.classList.add("table");
  }

  function showFallback(container) {
    container.replaceChildren();

    var message = document.createElement("p");
    message.textContent =
      "Current node availability could not be loaded in this page.";

    var link = document.createElement("a");
    link.href = SOURCE_URL;
    link.textContent = "View live KLC node availability";
    link.target = "_blank";
    link.rel = "noopener noreferrer";

    container.appendChild(message);
    container.appendChild(link);
  }

  function injectTable(container, table) {
    var imported = document.importNode(table, true);
    styleTable(imported);
    container.replaceChildren(imported);
  }

  function loadPlaceholders() {
    var placeholders = document.querySelectorAll("[data-klc-nodes]");

    if (!placeholders.length) {
      return;
    }

    fetch(SOURCE_URL, { cache: "no-cache" })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("HTTP " + response.status);
        }
        return response.text();
      })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, "text/html");

        placeholders.forEach(function (container) {
          var key = container.getAttribute("data-klc-nodes");
          var heading = HEADINGS[key];

          if (!heading) {
            showFallback(container);
            return;
          }

          var table = findTableAfterHeading(doc, heading);
          if (!table) {
            showFallback(container);
            return;
          }

          injectTable(container, table);
        });
      })
      .catch(function () {
        placeholders.forEach(showFallback);
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", loadPlaceholders);
  } else {
    loadPlaceholders();
  }
})();
