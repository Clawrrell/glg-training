/**
 * GLG Training Score Tracker — Google Apps Script
 * 
 * Deploy as a Web App:
 *   Execute as: Me (your Google account)
 *   Who has access: Anyone
 *
 * Sheet ID: 1_xaG5JVrTw84PscDE4kPmIv9dy86CFXKbJsc9ZT_fUo
 * Sheet tab: "Score Tracker"
 */

var SHEET_ID = "1_xaG5JVrTw84PscDE4kPmIv9dy86CFXKbJsc9ZT_fUo";
var SHEET_TAB = "Score Tracker";
var TEAMS_WEBHOOK = "https://default18c0a354c7674756852189afc5d7dd.ac.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/10928fd6e6bf475695e69aeeeb3a9c3c/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=nwOVrfWfkBDCd1j7tJNL1XJTDafST_2hBgKi3C1lhFQ";
var PASS_THRESHOLD = 0.70; // 70%

// ──────────────────────────────────────────────
// ENTRY POINT — handle POST requests from modules
// ──────────────────────────────────────────────
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    var employeeName = data.employeeName || "Unknown";
    var moduleId     = data.moduleId     || "unknown";
    var moduleName   = data.moduleName   || "Unknown Module";
    var score        = Number(data.score)    || 0;
    var maxScore     = Number(data.maxScore) || 100;
    var bonusScore   = Number(data.bonusScore) || 0;
    var maxStreak    = Number(data.maxStreak)  || 0;
    var badges       = data.badges       || '';
    var elapsedMin   = Number(data.elapsedMinutes) || 0;
    var passedAt     = data.passedAt     || new Date().toISOString();

    var pct     = maxScore > 0 ? Math.round((score / maxScore) * 100) : 0;
    var passed  = pct >= (PASS_THRESHOLD * 100);
    var status  = passed ? "Pass" : "Fail";
    var ts      = new Date(passedAt);

    // 1. Log to Google Sheet
    logToSheet(ts, employeeName, moduleId, moduleName, score, maxScore, bonusScore, pct, status, maxStreak, badges, elapsedMin);

    // 2. Send Teams notification
    notifyTeams(employeeName, moduleName, score, maxScore, pct, passed, ts);

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok" }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Allow simple GET ping to verify deployment is live
function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: "ok", message: "GLG Score Tracker is live" }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ──────────────────────────────────────────────
// LOG ROW TO GOOGLE SHEET
// ──────────────────────────────────────────────
function logToSheet(ts, employeeName, moduleId, moduleName, score, maxScore, bonusScore, pct, status, maxStreak, badges, elapsedMin) {
  var ss    = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(SHEET_TAB);

  // Create tab + header row if it doesn't exist yet
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_TAB);
    sheet.appendRow([
      "Timestamp",
      "Employee Name",
      "Module ID",
      "Module Name",
      "Score",
      "Max Score",
      "Bonus Score",
      "Percentage",
      "Pass/Fail",
      "Max Streak",
      "Badges",
      "Time (min)"
    ]);

    // Format header row
    var header = sheet.getRange(1, 1, 1, 12);
    header.setFontWeight("bold");
    header.setBackground("#141c2c");
    header.setFontColor("#ffffff");
    sheet.setFrozenRows(1);
  }

  sheet.appendRow([
    ts,
    employeeName,
    moduleId,
    moduleName,
    score,
    maxScore,
    bonusScore,
    pct + "%",
    status,
    maxStreak,
    badges,
    elapsedMin
  ]);
}

// ──────────────────────────────────────────────
// SEND ADAPTIVE CARD TO TEAMS VIA POWER AUTOMATE
// ──────────────────────────────────────────────
function notifyTeams(employeeName, moduleName, score, maxScore, pct, passed, ts) {
  var passColor  = passed ? "Good"      : "Attention";   // Adaptive Card accent
  var passLabel  = passed ? "✅  PASSED" : "❌  NEEDS REVIEW";
  var dateStr    = Utilities.formatDate(ts, Session.getScriptTimeZone(), "MMM d, yyyy h:mm a z");

  var adaptiveCard = {
    "type": "AdaptiveCard",
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.4",
    "body": [
      {
        "type": "Container",
        "style": passColor,
        "items": [
          {
            "type": "TextBlock",
            "text": "🎓 GLG Training Score Submitted",
            "weight": "Bolder",
            "size": "Medium"
          }
        ]
      },
      {
        "type": "FactSet",
        "facts": [
          { "title": "Employee",   "value": employeeName },
          { "title": "Module",     "value": moduleName },
          { "title": "Score",      "value": score + " / " + maxScore + "  (" + pct + "%)" },
          { "title": "Result",     "value": passLabel },
          { "title": "Submitted",  "value": dateStr }
        ]
      }
    ]
  };

  var payload = {
    "type": "message",
    "attachments": [
      {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": adaptiveCard
      }
    ]
  };

  var options = {
    method:      "post",
    contentType: "application/json",
    payload:     JSON.stringify(payload),
    muteHttpExceptions: true
  };

  UrlFetchApp.fetch(TEAMS_WEBHOOK, options);
}
