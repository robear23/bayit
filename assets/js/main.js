/* Bāyit Bagels - site behaviour. No dependencies. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  var BUSINESS_EMAIL = "oli.itkin@bayithospitality.co.uk";
  var LEAD_DAYS = 3;
  // 0 = Sunday ... 6 = Saturday. Open Tue-Sun 10:00-17:00, closed Monday.
  var HOURS = { 0: [10, 17], 1: null, 2: [10, 17], 3: [10, 17], 4: [10, 17], 5: [10, 17], 6: [10, 17] };
  var DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  function londonNow() {
    var parts = new Intl.DateTimeFormat("en-GB", {
      timeZone: "Europe/London", weekday: "short", hour: "numeric", minute: "numeric", hour12: false
    }).formatToParts(new Date());
    var get = function (t) { return (parts.find(function (p) { return p.type === t; }) || {}).value; };
    var dayIndex = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(get("weekday"));
    return { day: dayIndex, hour: parseInt(get("hour"), 10) % 24, minute: parseInt(get("minute"), 10) };
  }

  /* Open / closed status */
  function openStatus() {
    var now = londonNow();
    var today = HOURS[now.day];
    var t = now.hour + now.minute / 60;
    if (today && t >= today[0] && t < today[1]) {
      var left = today[1] - t;
      return { open: true, text: left <= 1 ? "Open now - closing soon" : "Open now, until 5pm" };
    }
    if (today && t < today[0]) return { open: false, text: "Closed - opens today at 10am" };
    for (var i = 1; i <= 7; i++) {
      var d = (now.day + i) % 7;
      if (HOURS[d]) return { open: false, text: "Closed - opens " + (i === 1 ? "tomorrow" : DAY_NAMES[d]) + " at 10am" };
    }
    return { open: false, text: "Closed" };
  }
  var status = openStatus();
  document.querySelectorAll("[data-open-status]").forEach(function (el) {
    el.textContent = status.text;
    el.classList.toggle("is-open", status.open);
  });
  var todayRow = document.querySelector('.hours tr[data-day="' + londonNow().day + '"]');
  if (todayRow) todayRow.classList.add("is-today");

  /* Mobile menu */
  var toggle = document.querySelector(".menu-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("menu-open")) {
        document.body.classList.remove("menu-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  /* Hero: the drawn bagel reveals a real one */
  var stack = document.querySelector(".bagel-stack");
  if (stack) {
    var photos = stack.querySelectorAll(".photo-oval img");
    var idx = 0;
    var cycleTimer = null;
    var show = function () {
      photos.forEach(function (p, i) { p.classList.toggle("is-active", i === idx); });
      stack.classList.add("is-revealed");
    };
    var hide = function () { stack.classList.remove("is-revealed"); };
    var next = function () { idx = (idx + 1) % photos.length; show(); };
    var startCycle = function () { show(); clearInterval(cycleTimer); cycleTimer = setInterval(next, 1600); };
    var stopCycle = function () { clearInterval(cycleTimer); hide(); };

    document.querySelectorAll("[data-reveal-trigger]").forEach(function (t) {
      t.addEventListener("mouseenter", startCycle);
      t.addEventListener("mouseleave", stopCycle);
      t.addEventListener("focus", startCycle);
      t.addEventListener("blur", stopCycle);
      t.addEventListener("click", function (e) {
        e.preventDefault();
        if (stack.classList.contains("is-revealed")) { next(); } else { startCycle(); clearInterval(cycleTimer); }
      });
    });
    // Touch screens never hover, so show one real bagel shortly after load.
    if (window.matchMedia("(hover: none)").matches) {
      setTimeout(function () { show(); }, 1400);
    }
  }

  /* Scroll reveals and line drawings */
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduceMotion) {
    document.querySelectorAll("[data-draw]").forEach(function (host) {
      host.querySelectorAll(".draw > *").forEach(function (shape) {
        if (typeof shape.getTotalLength !== "function") return;
        var len = Math.ceil(shape.getTotalLength()) + 1;
        shape.style.strokeDasharray = len;
        shape.style.strokeDashoffset = len;
      });
      host.classList.add("draw-ready");
    });
  }
  var observed = document.querySelectorAll(".reveal, [data-draw]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("is-inview"); io.unobserve(entry.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    observed.forEach(function (el) { io.observe(el); });
  } else {
    observed.forEach(function (el) { el.classList.add("is-inview"); });
  }

  /* Menu filters */
  var filterBtns = document.querySelectorAll(".filter");
  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var want = btn.getAttribute("data-filter");
      filterBtns.forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
      document.querySelectorAll(".item[data-diet]").forEach(function (item) {
        var diets = item.getAttribute("data-diet").split(" ");
        item.classList.toggle("is-hidden", want !== "all" && diets.indexOf(want) === -1);
      });
    });
  });

  /* Catering enquiry form: 3 days' notice, collection Tue-Sun */
  var form = document.querySelector("#enquiry-form");
  if (form) {
    var dateInput = form.querySelector("#date");
    var dateError = form.querySelector("#date-error");
    var statusEl = form.querySelector(".form-status");

    var earliest = new Date();
    earliest.setHours(0, 0, 0, 0);
    earliest.setDate(earliest.getDate() + LEAD_DAYS);
    while (!HOURS[earliest.getDay()]) earliest.setDate(earliest.getDate() + 1);
    var iso = function (d) {
      return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
    };
    dateInput.min = iso(earliest);
    var earliestLabel = document.querySelector("[data-earliest]");
    if (earliestLabel) {
      earliestLabel.textContent = earliest.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" });
    }

    var checkDate = function () {
      var msg = "";
      if (dateInput.value) {
        var picked = new Date(dateInput.value + "T00:00:00");
        if (picked < earliest) msg = "We need 3 days' notice - that's how long our dough takes. Earliest is " + earliest.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" }) + ".";
        else if (!HOURS[picked.getDay()]) msg = "We're closed on Mondays - please pick Tuesday to Sunday.";
      }
      dateError.textContent = msg;
      dateInput.closest(".field").classList.toggle("has-error", !!msg);
      return !msg;
    };
    dateInput.addEventListener("change", checkDate);

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!checkDate() || !form.reportValidity()) return;
      var data = new FormData(form);
      var type = data.get("type") || "Enquiry";
      var lines = [
        "Name: " + data.get("name"),
        "Email: " + data.get("email"),
        data.get("phone") ? "Phone: " + data.get("phone") : null,
        data.get("company") ? "Company / event: " + data.get("company") : null,
        "Type: " + type,
        "Date needed: " + data.get("date"),
        "Collection or delivery: " + data.get("handover"),
        "Number of people / bagels: " + data.get("quantity"),
        data.get("dietary") ? "Dietary needs: " + data.get("dietary") : null,
        "",
        data.get("message") || ""
      ].filter(function (l) { return l !== null; });
      var subject = type + " enquiry - " + data.get("date") + " - " + data.get("name");
      window.location.href = "mailto:" + BUSINESS_EMAIL +
        "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
      statusEl.textContent = "Opening your email app with everything filled in. Just press send.";
    });
  }

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
