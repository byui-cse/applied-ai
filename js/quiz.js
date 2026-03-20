/**
 * Inline quiz: mount into a container, fetch JSON by path relative to site root.
 */
(function () {
  "use strict";

  var FETCH_DOC = { cache: "no-store" };

  /** Fisher–Yates shuffle; returns a new permutation array of 0..n-1. */
  function shufflePermutation(n) {
    var perm = [];
    var i;
    for (i = 0; i < n; i++) {
      perm.push(i);
    }
    for (i = n - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = perm[i];
      perm[i] = perm[j];
      perm[j] = t;
    }
    return perm;
  }

  /**
   * Reorder choices for display. Maps original correctIndex through the permutation.
   * Set data.shuffleOptions to false to keep authored order.
   */
  function permuteChoices(choices, correctIndex, doShuffle) {
    var n = choices.length;
    if (!doShuffle || n <= 1) {
      return {
        choices: choices.slice(),
        correctIndex: correctIndex,
      };
    }
    var perm = shufflePermutation(n);
    var shuffled = perm.map(function (oldIdx) {
      return choices[oldIdx];
    });
    var newCorrect = perm.indexOf(correctIndex);
    return {
      choices: shuffled,
      correctIndex: newCorrect,
    };
  }

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  /** Delay (ms) after showing feedback before advancing to the next question or report. */
  var ADVANCE_MS = 1100;

  function renderQuiz(container, data) {
    var title = data.title || "Quiz";
    var intro = data.intro;
    var rawQuestions = Array.isArray(data.questions) ? data.questions : [];

    var html = "";
    html += '<div class="quiz" role="region" aria-label="' + escapeHtml(title) + '">';
    html += '<div class="quiz__head">';
    html += '<p class="quiz__label">Assessment</p>';
    html += '<p class="quiz__title">' + escapeHtml(title) + "</p>";
    if (intro) {
      html += '<p class="quiz__intro">' + escapeHtml(intro) + "</p>";
    }
    html += "</div>";

    if (!rawQuestions.length) {
      html += '<p class="quiz__empty">No questions in this quiz.</p>';
      html += "</div>";
      container.innerHTML = html;
      return;
    }

    var shuffleOn = data.shuffleOptions !== false;

    var prepared = rawQuestions.map(function (q) {
      var prompt = q.prompt || "";
      var rawChoices = Array.isArray(q.choices) ? q.choices : [];
      var rawCorrect = typeof q.correctIndex === "number" ? q.correctIndex : -1;
      var permuted = permuteChoices(rawChoices, rawCorrect, shuffleOn);
      return {
        prompt: prompt,
        choices: permuted.choices,
        correctIndex: permuted.correctIndex,
      };
    });

    html += '<div class="quiz__stage" aria-live="polite"></div>';
    html += "</div>";
    container.innerHTML = html;

    var stage = container.querySelector(".quiz__stage");
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
      var total = prepared.length;
      var correctCount = results.filter(function (r) {
        return r.correct;
      }).length;
      var reportTitle = data.reportTitle || "Your results";
      var out = "";
      out += '<div class="quiz__report">';
      out += '<p class="quiz__report-title">' + escapeHtml(reportTitle) + "</p>";
      out +=
        '<p class="quiz__report-summary">' +
        escapeHtml(
          "You answered " +
            correctCount +
            " of " +
            total +
            " correctly."
        ) +
        "</p>";
      out += '<ul class="quiz__report-list">';
      results.forEach(function (r) {
        out +=
          '<li class="quiz__report-item quiz__report-item--' +
          (r.correct ? "correct" : "incorrect") +
          '">';
        out +=
          '<span class="quiz__report-mark" aria-hidden="true">' +
          (r.correct ? "✓" : "✗") +
          "</span>";
        out += '<span class="quiz__report-item-text">';
        out +=
          '<span class="quiz__report-prompt">' +
          escapeHtml(r.prompt) +
          "</span>";
        out +=
          '<span class="quiz__report-status">' +
          escapeHtml(r.correct ? "Correct" : "Incorrect") +
          "</span>";
        out += "</span></li>";
      });
      out += "</ul></div>";
      stage.innerHTML = out;
    }

    function showQuestion(index) {
      clearAdvanceTimer();
      if (index >= prepared.length) {
        renderReport(state.results);
        return;
      }

      var q = prepared[index];
      var qid = "quiz-q-" + index + "-" + Math.random().toString(36).slice(2, 8);
      var choices = q.choices;
      var correct = q.correctIndex;
      var prompt = q.prompt;

      var body = "";
      body +=
        '<p class="quiz__progress">Question <span class="quiz__progress-current">' +
        (index + 1) +
        '</span> of <span class="quiz__progress-total">' +
        prepared.length +
        "</span></p>";
      body += '<fieldset class="quiz__question">';
      body += '<legend class="quiz__prompt">' + escapeHtml(prompt) + "</legend>";
      if (!choices.length) {
        body += '<p class="quiz__empty">Missing choices.</p>';
      } else {
        choices.forEach(function (choice, ci) {
          body += '<label class="quiz__choice">';
          body +=
            '<input type="radio" name="' +
            qid +
            '" value="' +
            ci +
            '" data-correct="' +
            (ci === correct ? "1" : "0") +
            '" />';
          body +=
            '<span class="quiz__choice-text">' +
            escapeHtml(String(choice)) +
            "</span>";
          body += "</label>";
        });
      }
      body += '<div class="quiz__feedback" hidden></div>';
      body += "</fieldset>";
      stage.innerHTML = body;

      var fieldset = stage.querySelector(".quiz__question");
      if (!fieldset) return;

      fieldset.addEventListener("change", function onChange(e) {
        var input = e.target;
        if (!input || input.type !== "radio") return;
        fieldset.removeEventListener("change", onChange);
        var feedbackEl = fieldset.querySelector(".quiz__feedback");
        var isCorrect = input.getAttribute("data-correct") === "1";
        if (feedbackEl) {
          feedbackEl.hidden = false;
          feedbackEl.className =
            "quiz__feedback quiz__feedback--" + (isCorrect ? "correct" : "incorrect");
          feedbackEl.textContent = isCorrect
            ? data.feedbackCorrect || "Correct."
            : data.feedbackIncorrect ||
              "Not quite — review the definitions above.";
        }
        fieldset.querySelectorAll('input[type="radio"]').forEach(function (r) {
          r.disabled = true;
        });
        state.results.push({ correct: isCorrect, prompt: prompt });
        advanceTimer = setTimeout(function () {
          advanceTimer = null;
          state.index = index + 1;
          showQuestion(state.index);
        }, ADVANCE_MS);
      });
    }

    showQuestion(0);
  }

  function mount(container, jsonPath, indexDir) {
    if (!container || !jsonPath) return;
    container.innerHTML = '<p class="quiz__loading">Loading quiz…</p>';
    var url;
    try {
      url = new URL(jsonPath, indexDir);
    } catch {
      container.innerHTML =
        '<p class="prose prose--error">Invalid quiz URL.</p>';
      return;
    }
    fetch(url, FETCH_DOC)
      .then(function (res) {
        if (!res.ok) throw new Error(String(res.status));
        return res.json();
      })
      .then(function (data) {
        renderQuiz(container, data);
      })
      .catch(function () {
        container.innerHTML =
          '<p class="prose prose--error">Could not load this quiz.</p>';
      });
  }

  window.AppliedAIQuiz = { mount: mount };
})();
