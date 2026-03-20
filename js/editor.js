/**
 * Markdown editor + preview: mount into a container, fetch JSON under assessments/.
 * Variant "markdown-with-preview": split editor, compare to expected markdown (character-based).
 */
(function () {
  "use strict";

  var FETCH_DOC = { cache: "no-store" };
  var ADVANCE_MS = 1400;

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  /** Trim ends and normalize line endings for fair comparison. */
  function normalizeMarkdown(s) {
    return String(s || "")
      .replace(/\r\n/g, "\n")
      .replace(/\r/g, "\n")
      .trim();
  }

  /** Levenshtein distance (iterative, full matrix). */
  function levenshtein(a, b) {
    var m = a.length;
    var n = b.length;
    if (m === 0) return n;
    if (n === 0) return m;
    var i;
    var j;
    var prev = [];
    var cur = [];
    for (j = 0; j <= n; j++) {
      prev[j] = j;
    }
    for (i = 1; i <= m; i++) {
      cur[0] = i;
      var ai = a.charCodeAt(i - 1);
      for (j = 1; j <= n; j++) {
        var cost = ai === b.charCodeAt(j - 1) ? 0 : 1;
        cur[j] = Math.min(
          prev[j] + 1,
          cur[j - 1] + 1,
          prev[j - 1] + cost
        );
      }
      var t = prev;
      prev = cur;
      cur = t;
    }
    return prev[n];
  }

  /** 0–100: higher is closer to the expected string. */
  function characterCorrectnessPercent(student, expected) {
    var a = normalizeMarkdown(student);
    var b = normalizeMarkdown(expected);
    if (a === b) return 100;
    var maxLen = Math.max(a.length, b.length, 1);
    var d = levenshtein(a, b);
    return Math.max(0, Math.min(100, Math.round(100 * (1 - d / maxLen))));
  }

  function parseMarkdown(html) {
    if (typeof marked !== "undefined" && typeof marked.parse === "function") {
      return marked.parse(html);
    }
    return "<p>" + escapeHtml(html) + "</p>";
  }

  function renderEditor(container, data) {
    var title = data.title || "Editor";
    var intro = data.intro;
    var reportTitle = data.reportTitle || "Your results";
    var raw = Array.isArray(data.challenges) ? data.challenges : [];
    var tolerance =
      typeof data.matchTolerancePercent === "number"
        ? data.matchTolerancePercent
        : 80;

    var html = "";
    html += '<div class="md-editor" role="region" aria-label="' + escapeHtml(title) + '">';
    html += '<div class="md-editor__head">';
    html += '<p class="md-editor__label">Practice</p>';
    html += '<p class="md-editor__title">' + escapeHtml(title) + "</p>";
    if (intro) {
      html += '<p class="md-editor__intro">' + escapeHtml(intro) + "</p>";
    }
    html += "</div>";

    if (!raw.length) {
      html += '<p class="md-editor__empty">No challenges configured.</p>';
      html += "</div>";
      container.innerHTML = html;
      return;
    }

    var challenges = raw.slice(0, 3).map(function (c) {
      return {
        prompt: c.prompt || "",
        expectedMarkdown: c.expectedMarkdown != null ? String(c.expectedMarkdown) : "",
      };
    });

    html += '<div class="md-editor__stage" aria-live="polite"></div>';
    html += "</div>";
    container.innerHTML = html;

    var stage = container.querySelector(".md-editor__stage");
    var advanceTimer = null;
    var state = {
      index: 0,
      results: [],
    };

    function clearAdvanceTimer() {
      if (advanceTimer !== null) {
        clearTimeout(advanceTimer);
        advanceTimer = null;
      }
    }

    function renderReport(results) {
      var total = challenges.length;
      var passCount = results.filter(function (r) {
        return r.pass;
      }).length;
      var out = "";
      out += '<div class="md-editor__report">';
      out += '<p class="md-editor__report-title">' + escapeHtml(reportTitle) + "</p>";
      out +=
        '<p class="md-editor__report-summary">' +
        escapeHtml(
          "You matched " +
            passCount +
            " of " +
            total +
            " challenges at or above the required accuracy."
        ) +
        "</p>";
      out += '<ul class="md-editor__report-list">';
      results.forEach(function (r) {
        out +=
          '<li class="md-editor__report-item md-editor__report-item--' +
          (r.pass ? "pass" : "fail") +
          '">';
        out +=
          '<span class="md-editor__report-mark" aria-hidden="true">' +
          (r.pass ? "✓" : "✗") +
          "</span>";
        out += '<span class="md-editor__report-item-text">';
        out +=
          '<span class="md-editor__report-prompt">' +
          escapeHtml(r.prompt) +
          "</span>";
        out +=
          '<span class="md-editor__report-status">' +
          escapeHtml(
            r.pass
              ? "Met target (" + r.percent + "%)"
              : r.percent + "% (needed " + tolerance + "%)"
          ) +
          "</span>";
        out += "</span></li>";
      });
      out += "</ul></div>";
      stage.innerHTML = out;
    }

    function showChallenge(index) {
      clearAdvanceTimer();
      if (index >= challenges.length) {
        renderReport(state.results);
        return;
      }

      var ch = challenges[index];
      var prompt = ch.prompt;
      var expected = ch.expectedMarkdown;
      var targetHtml = parseMarkdown(expected);

      var body = "";
      body +=
        '<p class="md-editor__progress">Challenge <span class="md-editor__progress-current">' +
        (index + 1) +
        '</span> of <span class="md-editor__progress-total">' +
        challenges.length +
        "</span></p>";

      body += '<p class="md-editor__prompt">' + escapeHtml(prompt) + "</p>";

      body += '<div class="md-editor__target">';
      body += '<p class="md-editor__target-label">Target preview</p>';
      body +=
        '<div class="md-editor__target-preview prose">' +
        targetHtml +
        "</div>";
      body += "</div>";

      body += '<div class="md-editor__split">';
      body += '<div class="md-editor__pane md-editor__pane--input">';
      body += '<label class="md-editor__pane-label" for="md-editor-ta">Your markdown</label>';
      body +=
        '<textarea id="md-editor-ta" class="md-editor__textarea" rows="12" spellcheck="false" aria-describedby="md-editor-hint"></textarea>';
      body +=
        '<p id="md-editor-hint" class="md-editor__hint">Match the target using markdown. Your preview updates as you type.</p>';
      body += "</div>";
      body += '<div class="md-editor__pane md-editor__pane--preview">';
      body += '<p class="md-editor__pane-label">Your preview</p>';
      body += '<div class="md-editor__live-preview prose"></div>';
      body += "</div>";
      body += "</div>";

      body += '<div class="md-editor__actions">';
      body +=
        '<button type="button" class="md-editor__submit">Submit</button>';
      body += "</div>";
      body += '<div class="md-editor__feedback" hidden></div>';

      stage.innerHTML = body;

      var ta = stage.querySelector(".md-editor__textarea");
      var live = stage.querySelector(".md-editor__live-preview");
      var submitBtn = stage.querySelector(".md-editor__submit");
      var feedbackEl = stage.querySelector(".md-editor__feedback");

      function updatePreview() {
        if (!live) return;
        live.innerHTML = parseMarkdown(ta ? ta.value : "");
      }

      if (ta) {
        ta.addEventListener("input", updatePreview);
        updatePreview();
        ta.focus();
      }

      function onSubmit() {
        if (!ta || !feedbackEl || !submitBtn) return;
        var pct = characterCorrectnessPercent(ta.value, expected);
        var pass = pct >= tolerance;
        submitBtn.disabled = true;
        ta.readOnly = true;

        feedbackEl.hidden = false;
        feedbackEl.className =
          "md-editor__feedback md-editor__feedback--" + (pass ? "pass" : "miss");
        feedbackEl.innerHTML =
          "<p><strong>" +
          (pass ? "Match." : "Not quite.") +
          "</strong> Character closeness: " +
          pct +
          "% (target: " +
          tolerance +
          "% or higher).</p>";

        state.results.push({
          prompt: prompt,
          percent: pct,
          pass: pass,
        });

        advanceTimer = setTimeout(function () {
          advanceTimer = null;
          state.index = index + 1;
          showChallenge(state.index);
        }, ADVANCE_MS);
      }

      if (submitBtn) {
        submitBtn.addEventListener("click", onSubmit);
      }
    }

    showChallenge(0);
  }

  function mount(container, jsonPath, indexDir, variant) {
    if (!container || !jsonPath) return;
    if (variant !== "markdown-with-preview") {
      container.innerHTML =
        '<p class="prose prose--error">Unknown editor variant.</p>';
      return;
    }
    container.innerHTML = '<p class="md-editor__loading">Loading…</p>';
    var url;
    try {
      url = new URL(jsonPath, indexDir);
    } catch {
      container.innerHTML =
        '<p class="prose prose--error">Invalid editor URL.</p>';
      return;
    }
    fetch(url, FETCH_DOC)
      .then(function (res) {
        if (!res.ok) throw new Error(String(res.status));
        return res.json();
      })
      .then(function (data) {
        renderEditor(container, data);
      })
      .catch(function () {
        container.innerHTML =
          '<p class="prose prose--error">Could not load this exercise.</p>';
      });
  }

  window.AppliedAIEditor = { mount: mount };
})();
