/**
 * GLG Training Score Tracker — Module-Side JavaScript
 *
 * Include this file in every training module (or paste inline).
 * After the Apps Script is deployed, replace TRACKER_URL with the real web app URL.
 *
 * Usage:
 *   submitTrainingScore("Sydney", "day5", "Week 1 Mastery Challenge", 175, 200);
 */

// ─── REPLACE THIS URL after deploying the Apps Script web app ───────────────
var TRACKER_URL = "YOUR_APPS_SCRIPT_WEB_APP_URL_HERE";
// ────────────────────────────────────────────────────────────────────────────

/**
 * submitTrainingScore
 *
 * @param {string} employeeName  - Full name entered by employee
 * @param {string} moduleId      - Short identifier, e.g. "day5"
 * @param {string} moduleName    - Human-readable name, e.g. "Week 1 Mastery Challenge"
 * @param {number} score         - Points earned
 * @param {number} maxScore      - Maximum possible points
 */
function submitTrainingScore(employeeName, moduleId, moduleName, score, maxScore) {
  // Validate URL is configured
  if (!TRACKER_URL || TRACKER_URL === "YOUR_APPS_SCRIPT_WEB_APP_URL_HERE") {
    console.warn("[Score Tracker] Tracker URL not configured — score NOT submitted.");
    showScoreConfirmation(false, "Score tracker not yet configured. Please notify IT.");
    return;
  }

  var payload = {
    employeeName: employeeName,
    moduleId:     moduleId,
    moduleName:   moduleName,
    score:        score,
    maxScore:     maxScore,
    passedAt:     new Date().toISOString()
  };

  fetch(TRACKER_URL, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify(payload),
    // No-cors because Apps Script redirects; we can't read the response body
    // but the POST still goes through.
    mode:    "no-cors"
  })
  .then(function() {
    showScoreConfirmation(true);
  })
  .catch(function(err) {
    console.error("[Score Tracker] Submission failed:", err);
    showScoreConfirmation(false, "Network error — please email results as backup.");
  });
}

/**
 * showScoreConfirmation
 * Looks for #score-confirmation in the DOM and shows it.
 * Falls back to alert if element not found.
 */
function showScoreConfirmation(success, customMessage) {
  var el = document.getElementById("score-confirmation");
  if (el) {
    el.style.display = "block";
    if (!success && customMessage) {
      el.innerHTML = "⚠️ " + customMessage;
      el.style.background = "#fff3cd";
      el.style.borderLeftColor = "#f39c12";
      el.style.color = "#856404";
    }
  } else {
    if (success) {
      alert("Score submitted! Your results have been recorded.");
    } else {
      alert(customMessage || "Score submission failed. Please email results as backup.");
    }
  }
}
