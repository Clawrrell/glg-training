# GLG Training Score Tracker — Setup Guide

> **Time required:** ~10 minutes  
> **Who does this:** Harrell (one-time setup)  
> **After setup:** Scores flow automatically into your Google Sheet + Teams notification on every module completion.

---

## What This Does

When a trainee finishes a module and submits their name, their score is automatically:

1. ✅ Logged to your Google Sheet (with timestamp, name, score, pass/fail)
2. 🔔 Sent as a Teams notification (Adaptive Card format)

---

## STEP 1 — Open the Google Sheet

1. Go to: [https://docs.google.com/spreadsheets/d/1_xaG5JVrTw84PscDE4kPmIv9dy86CFXKbJsc9ZT_fUo](https://docs.google.com/spreadsheets/d/1_xaG5JVrTw84PscDE4kPmIv9dy86CFXKbJsc9ZT_fUo)
2. Make sure you are logged in with your Google account that owns this sheet.

---

## STEP 2 — Open Apps Script

1. In the spreadsheet menu, click **Extensions** (top menu bar)
2. Click **Apps Script**
3. A new browser tab opens — this is the Apps Script editor

*(Screenshot: You'll see a text editor with a default `function myFunction(){}` — you'll replace all of this.)*

---

## STEP 3 — Paste the Code

1. Select **all** the existing code in the editor (Ctrl+A / Cmd+A)
2. **Delete** it
3. Open the file: `glg/training-modules/apps_script_tracker.js` (or copy from below)
4. Paste the entire contents into the editor
5. Click the **💾 Save** button (floppy disk icon, or Ctrl+S / Cmd+S)
6. Name the project **"GLG Score Tracker"** when prompted → click OK

---

## STEP 4 — Deploy as a Web App

1. Click the blue **Deploy** button (top right)
2. Select **New deployment**
3. Click the gear icon ⚙️ next to "Select type" → choose **Web app**
4. Fill in the settings:
   - **Description:** GLG Training Score Tracker
   - **Execute as:** Me (your Google account)
   - **Who has access:** Anyone
5. Click **Deploy**
6. Google will ask you to **Authorize access** — click **Authorize**, then choose your Google account, and click **Allow** on the permissions screen
7. After deploying, you'll see a **Web app URL** — it looks like:
   ```
   https://script.google.com/macros/s/AKfycby.../exec
   ```
8. **Copy that URL** — you need it in the next step.

---

## STEP 5 — Update the Module JavaScript

Open the module file in a text editor (or let Claw do it):

**File:** `glg/training-modules/module-day5-week1-review-v2.html`

Find this line near the bottom of the `<script>` section:
```javascript
var TRACKER_URL = 'YOUR_APPS_SCRIPT_WEB_APP_URL_HERE';
```

Replace with your actual URL:
```javascript
var TRACKER_URL = 'https://script.google.com/macros/s/YOUR_ACTUAL_ID/exec';
```

Do the same in `score_tracker.js` for future modules.

---

## STEP 6 — Push to GitHub (if not already done)

```bash
cd /Users/harrellgunn/.openclaw/workspace/glg/training-modules
git add -A
git commit -m "Set live tracker URL"
git push origin main
```

GitHub Pages will update in ~30 seconds.

---

## STEP 7 — Verify It Works

1. Open the live Day 5 module in a browser
2. Complete a few questions (or jump to the Feedback section)
3. Enter a test name (e.g. "Test User") → click "Submit Score & View Certificate"
4. Check the Google Sheet — a new row should appear under the "Score Tracker" tab
5. Check Teams — a notification card should appear

---

## Google Sheet Column Layout

The "Score Tracker" tab is created automatically on first submission with these columns:

| Column | Data |
|--------|------|
| A | Timestamp |
| B | Employee Name |
| C | Module ID (e.g. `day5`) |
| D | Module Name |
| E | Score (points earned) |
| F | Max Score |
| G | Percentage |
| H | Pass / Fail (Pass = 70%+) |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Score not appearing in sheet | Re-check the TRACKER_URL in the HTML file matches the deployed URL exactly |
| "Authorization required" error | Re-deploy the Apps Script — make sure "Execute as: Me" is selected |
| Teams notification not arriving | The Power Automate webhook URL may have expired — check with IT |
| Old URL cached | After updating the URL, hard-refresh the module page (Ctrl+Shift+R) |

---

## Adding Score Tracking to Future Modules

1. Copy the `submitScoreAndBuildCert()` block from `module-day5-week1-review-v2.html` into the new module
2. Change `moduleId` and `moduleName` to match the new module
3. Update `maxScore` if the point scale is different
4. Add the name input form and `#score-confirmation` div to the completion page
5. Set `TRACKER_URL` to the same deployed URL (it works for all modules)

Or simply include `score_tracker.js` in future modules and call:
```javascript
submitTrainingScore(employeeName, "day6", "Medical Records Deep Dive", score, maxScore);
```

---

## BACKFILL TRACKER — Days 1-8 Score Submit Bug (Opened June 15, 2026)

**Issue:** Modules Day 1-8 submit `totalScore + bonusScore` as the `score` field but set `maxScore: 200` (base only). This produces >100% scores in the tracker (e.g., 297/200).

**Root cause:** `submitScoreAndBuildCert()` in all 8 deployed modules uses `state.totalScore + state.bonusScore` as the score value.

**Additional complexity:** Day 5 matching exercise awards `Math.round(10/3)` = 3 pts per match (9 pts for 3/3 perfect), breaking the 5-pt granularity. Section point headers ("Up to 50 pts") may not match actual question counts in some modules.

**Fix required in each module:**
1. Change submit to send `state.totalScore` (base only) as `score`
2. Send `state.bonusScore` as separate `bonusScore` field
3. Audit maxScore value against actual question count × 10 + matching pts
4. Redeploy all 8 modules to site/ and push to GitHub Pages

**Status:** NOT STARTED — separate workstream from Day 9/10 build
**Deadline:** Before Janeth starts (June 23)
**Priority:** Must complete before any new hire runs Days 1-8, or scores will be wrong again

**Sydney's existing scores:** Cannot be decomposed from tracker data. The tracker received one combined number per module. No per-question attempt log exists. Her actual base scores are unrecoverable unless she retakes the modules.

---

## PER-QUESTION EVENT LOG — Engine Change (Opened June 15, 2026)

**Issue:** No per-question data is persisted. The scoring engine tracks attempt state client-side only (`state.answered`, `state.answeredWrong`) but sends ONE aggregate POST at completion. If a trainee's competency is ever challenged, there is no audit trail showing which questions they got right/wrong, how many attempts per question, or time-per-question.

**What the audit trail needs per question:**
- `questionId` (e.g., "q1")
- `attemptCount` (1 = first try, 2 = second try, etc.)
- `pointsAwarded` (base only)
- `bonusAwarded` (separate)
- `timeToAnswer` (seconds from question display to correct answer)
- `sectionId`

**Implementation options:**
1. **Batch POST at end:** Collect per-question events in an array during the quiz, send the full array alongside the summary at submit time. Apps Script writes to a separate "Question Log" sheet tab.
2. **Real-time POST per question:** Each answer fires a POST immediately. More resilient to browser close, but heavier on Apps Script quota.

**Recommendation:** Option 1 (batch at end) — simpler, same data, one round-trip.

**Schema change required:** New sheet tab "Question Log" with columns: Timestamp, Employee Name, Module ID, Question ID, Attempt Count, Points Awarded, Bonus Awarded, Time To Answer (s), Correct On First Try (Y/N)

**Status:** NOT STARTED — separate from submit fix
**Deadline:** Before Janeth starts (June 23)
**Priority:** HIGH — this is the one that protects the firm if training is challenged downstream
**Scope:** All modules (Days 1-10 at minimum, ideally all future modules built with this from the start)

---

## BRAIN-SCRUB WORKSTREAM — Reference Docs (Opened June 15, 2026)

**Scope:** Run operations SOPs and training reference docs through the proprietary brain (Systems 1-4 + book memos per TASK-FRAMEWORK-MAP) so training ships brain-processed material, not raw BYPASS docs.
**Classification:** System 3 work. Not part of onboarding build.
**Status:** HELD — pending dedicated session with Harrell
**Owner:** COO seat
**Deadline:** TBD (not June 23 — separate from onboarding track)
**Docs in scope (Sydney's Day 9 set, first priority):**
1. Communication_Logging_Standards
2. New_Client_Welcome_Call_Script
3. Treatment_Check_In_Call_Script
4. Treatment_Gap_Call_Script
5. Demand_Update_Call_Script
6. Settlement_Offer_Call_Script
7. Settlement_Acceptance_Call_Script
8. Litigation_Handoff_Call_Script
9. Case_Drop_Call_Script
10. Client_Difficult_Conversation_Guide
**Rule:** Do NOT start without explicit go-ahead from Harrell.

---

## STANDALONE .DOCX — Templates, Letters, Forms (Opened June 15, 2026)

**Issue:** ~15 .docx files in canonical-sops/docx/ have no .md counterpart — they are unique client-facing templates, letters, and forms (e.g., Client_Disengagement_Letter, New_Client_Welcome_Letter_template, Spoliation_Letter, etc.). These are high-stakes client-facing material.
**Scope:** Surface options for handling .docx natively before assuming a path. Cannot brain-scrub .docx directly via current tooling.
**Status:** NOT STARTED — separate workstream
**Owner:** COO seat
**Deadline:** TBD (not today)

---

## SOURCE .DOCX ARCHIVE POLICY (Opened June 15, 2026)

**Issue:** ~245 .docx files are source copies of docs that now have brain-processed .md versions. Once .md scrubs are verified complete with MANIFESTs, source .docx copies need a clear archive label and the .md becomes canonical.
**Scope:** Label .docx as "SOURCE — canonical version is .md", confirm no content drift between .docx original and .md scrubbed version.
**Status:** NOT STARTED — depends on scrub completion
**Owner:** COO seat
**Deadline:** After scrub completes
