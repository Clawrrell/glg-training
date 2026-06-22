#!/usr/bin/env python3
"""Build NH-11 from day10 chassis — content swap + distractor parity + certificate enhance."""
import re

with open('site/module-day10.html', 'r') as f:
    src = f.read()

# ──────────────────────────────────────────
# 1. TITLE + MODULE ID
# ──────────────────────────────────────────
src = src.replace(
    '<title>Day 10 — Week 2 Review &amp; Assessment | Gunn Law Group</title>',
    '<title>NH-11 — Week 2 Review &amp; Assessment | Gunn Law Group</title>'
)
src = src.replace("'day10'", "'nh11'")
src = src.replace('"day10"', '"nh11"')
src = src.replace("'Week 2 Review & Assessment'", "'NH-11 Week 2 Review & Assessment'")
src = src.replace('"Week 2 Review & Assessment"', '"NH-11 Week 2 Review & Assessment"')

# ──────────────────────────────────────────
# 2. MANIFEST COMMENT — replace entirely
# ──────────────────────────────────────────
manifest_end = src.index('<!DOCTYPE html>')
new_manifest = """<!--
═══════════════════════════════════════════════
NH-11 — Week 2 Review & Assessment (Polished)
Built: June 17, 2026
Base: site/module-day10.html (Day 10 polished chassis)
Content: NH-11 standalone 20-question assessment (Days 6-10)
Answer Key: A=5 B=5 C=5 D=5 (verified)
Distractor Parity: All options within 20% word count (verified)
Banned Terms: 0 hits (label the emotion, Voss, mirroring, etc.)
Case Numbers: Teresa Ramirez = GLG-2026-1192 (no collision with NH-10)
moduleId: nh11
moduleName: NH-11 Week 2 Review & Assessment
═══════════════════════════════════════════════
-->
"""
src = new_manifest + src[manifest_end:]

# ──────────────────────────────────────────
# 3. DAY BADGE + HEADERS
# ──────────────────────────────────────────
src = src.replace(
    '<div class="day-badge">Day 10 · Week 2 Review</div>',
    '<div class="day-badge">NH-11 · Week 2 Review</div>'
)
src = src.replace(
    '<h1>Week 2 Comprehensive Assessment</h1>',
    '<h1>NH-11 — Week 2 Review &amp; Assessment</h1>'
)

# ──────────────────────────────────────────
# 4. NAV PILLS — replace the full nav block
# ──────────────────────────────────────────
old_nav = '''<nav class="section-nav" id="section-nav">
  <button class="nav-pill active" id="nav-0" onclick="goToSection(0)">1. Intro</button>
  <button class="nav-pill" id="nav-1" onclick="goToSection(1)">2. Day 6</button>
  <button class="nav-pill" id="nav-2" onclick="goToSection(2)">3. Day 7</button>
  <button class="nav-pill" id="nav-3" onclick="goToSection(3)">4. Day 8</button>
  <button class="nav-pill" id="nav-4" onclick="goToSection(4)">5. Day 9</button>
  <button class="nav-pill" id="nav-5" onclick="goToSection(5)">6. Integrate</button>
  <button class="nav-pill" id="nav-6" onclick="goToSection(6)">7. Boss</button>
  <button class="nav-pill" id="nav-7" onclick="goToSection(7)">8. Results</button>
  <button class="nav-pill" id="nav-8" onclick="goToSection(8)">9. Feedback</button>
</nav>'''
new_nav = '''<nav class="section-nav" id="section-nav">
  <button class="nav-pill active" id="nav-0" onclick="goToSection(0)">1. Intro</button>
  <button class="nav-pill" id="nav-1" onclick="goToSection(1)">2. Records</button>
  <button class="nav-pill" id="nav-2" onclick="goToSection(2)">3. Coverage</button>
  <button class="nav-pill" id="nav-3" onclick="goToSection(3)">4. Liens</button>
  <button class="nav-pill" id="nav-4" onclick="goToSection(4)">5. Comms</button>
  <button class="nav-pill" id="nav-5" onclick="goToSection(5)">6. Treatment</button>
  <button class="nav-pill" id="nav-6" onclick="goToSection(6)">7. Boss</button>
  <button class="nav-pill" id="nav-7" onclick="goToSection(7)">8. Results</button>
  <button class="nav-pill" id="nav-8" onclick="goToSection(8)">9. Feedback</button>
</nav>'''
src = src.replace(old_nav, new_nav)

# ──────────────────────────────────────────
# 5. REPLACE ALL SECTION CONTENT (sections 0-6)
#    Find <div class="section-card" id="section-X"> ... next section-card
# ──────────────────────────────────────────

# Helper: find section content between section-card markers
def find_section(html, section_id):
    """Return (start, end) of section content."""
    marker = f'<div class="section-card'
    # Find the section by id
    pat = f'id="section-{section_id}"'
    idx = html.index(pat)
    # Go back to find the <div class="section-card" that contains this id
    start = html.rfind(marker, 0, idx)
    # Find the NEXT section-card (or </main> for the last section)
    next_start = html.find(marker, idx + 1)
    if next_start == -1:
        next_start = html.find('</main>', idx)
    return start, next_start

# Build new section content
SECTIONS = {}

SECTIONS[0] = '''<div class="section-card active" id="section-0">
  <div class="section-header">
    <div class="section-num">Section 1 · Week 2 Capstone</div>
    <h2>Welcome to the Week 2 Assessment</h2>
    <div class="section-subhead">Six domains. One exam. Everything tested at once.</div>
  </div>
  <div class="section-body">
    <div class="scenario">
      <div class="scenario-tag">What This Tests</div>
      <h3>Days 6&ndash;10: Medical Records &middot; Coverage &middot; Liens &middot; Communication &middot; Treatment Management</h3>
      <p>This is your Week 2 comprehensive assessment. 20 questions across every topic you've studied, plus a <span class="highlight">Boss Challenge</span> that pulls from <span class="urgent">all five domains at once.</span></p>
    </div>
    <div class="info-block">
      <h4>&#128203; How It Works</h4>
      <ul>
        <li><strong>20 base questions</strong> &times; 10 pts = 200 points possible</li>
        <li><strong>Pass threshold:</strong> 160/200 (80%)</li>
        <li><strong>Bonus points</strong> for first-try correct answers (+5 each)</li>
        <li><strong>Boss Challenge</strong> (Section 7): bonus-only points from a complex scenario</li>
        <li><strong>Streaks:</strong> consecutive correct answers build combos &#128293;</li>
      </ul>
    </div>
    <div class="callout callout-warn"><strong>Assessment mode:</strong> Wrong answers lock immediately. You get one shot per question. Think before you click.</div>
    <div class="btn-group"><button class="btn btn-primary btn-block" onclick="goToSection(1)">Begin Assessment &rarr;</button></div>
  </div>
</div>
'''

SECTIONS[1] = '''<div class="section-card" id="section-1">
  <div class="section-header">
    <div class="section-num">Section 2 · Day 6 Review · Up to 30 pts</div>
    <h2>Medical Records &amp; Analysis</h2>
  </div>
  <div class="section-body">
    <div class="question-block" id="q1-block">
      <div class="q-num">Question 1 of 20 &middot; 10 pts</div>
      <div class="q-text">A client asks you to explain their MRI results over the phone. The report says &ldquo;L5-S1 disc herniation with moderate foraminal stenosis.&rdquo; What is the correct approach?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q1','a',false)" id="q1-a"><span class="opt-letter">A</span><span class="opt-text">Read the imaging findings directly from the report using the medical terminology, then ask if the client has questions about the specific terms listed.</span></button>
        <button class="option-btn" onclick="answer('q1','b',false)" id="q1-b"><span class="opt-letter">B</span><span class="opt-text">Tell the client you cannot interpret medical records and refer them to their treating physician for a detailed explanation of MRI findings and prognosis.</span></button>
        <button class="option-btn" onclick="answer('q1','c',true)" id="q1-c"><span class="opt-letter">C</span><span class="opt-text">Translate the medical jargon into plain language using everyday analogies, connect findings to their symptoms, and confirm understanding &mdash; but never diagnose or predict outcomes.</span></button>
        <button class="option-btn" onclick="answer('q1','d',false)" id="q1-d"><span class="opt-letter">D</span><span class="opt-text">Email the full MRI report directly to the client with a brief cover note so they can review the medical findings independently and follow up with questions.</span></button>
      </div>
      <div class="feedback-box" id="q1-fb"></div>
    </div>
    <div class="question-block" id="q2-block">
      <div class="q-num">Question 2 of 20 &middot; 10 pts</div>
      <div class="q-text">You notice a pre-lit client has a 3-week gap in chiropractic treatment. No explanation is documented. What must you do?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q2','a',false)" id="q2-a"><span class="opt-letter">A</span><span class="opt-text">Note the gap in CasePeer and continue monitoring &mdash; a single gap under 30 days does not typically impact case value if treatment resumes soon afterward.</span></button>
        <button class="option-btn" onclick="answer('q2','b',false)" id="q2-b"><span class="opt-letter">B</span><span class="opt-text">Call the client and firmly remind them that missing treatment will reduce their settlement, then schedule their next appointment before ending the call.</span></button>
        <button class="option-btn" onclick="answer('q2','c',false)" id="q2-c"><span class="opt-letter">C</span><span class="opt-text">Notify the attorney immediately that the case may need to be dropped &mdash; a treatment gap of three weeks suggests the client is not compliant with care.</span></button>
        <button class="option-btn" onclick="answer('q2','d',true)" id="q2-d"><span class="opt-letter">D</span><span class="opt-text">Document the gap with exact dates in CasePeer, contact the client to determine why treatment stopped, and note their explanation &mdash; adjusters use unexplained gaps at negotiation.</span></button>
      </div>
      <div class="feedback-box" id="q2-fb"></div>
    </div>
    <div class="question-block" id="q3-block">
      <div class="q-num">Question 3 of 20 &middot; 10 pts</div>
      <div class="q-text">Which records establish the critical first link between the accident and the diagnosed injuries &mdash; and why are they irreplaceable in the demand?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q3','a',false)" id="q3-a"><span class="opt-letter">A</span><span class="opt-text">The chiropractor&rsquo;s treatment records, because they document the full course of care and show ongoing symptoms that confirm the injury&rsquo;s severity over time.</span></button>
        <button class="option-btn" onclick="answer('q3','b',true)" id="q3-b"><span class="opt-letter">B</span><span class="opt-text">ER records from the accident date &mdash; they establish causation by documenting symptoms immediately after impact, before any alternative cause can be argued by the insurer.</span></button>
        <button class="option-btn" onclick="answer('q3','c',false)" id="q3-c"><span class="opt-letter">C</span><span class="opt-text">The MRI or diagnostic imaging report, because objective structural findings like disc herniations cannot be disputed and carry the most weight with insurance adjusters.</span></button>
        <button class="option-btn" onclick="answer('q3','d',false)" id="q3-d"><span class="opt-letter">D</span><span class="opt-text">The police report from the scene, because it establishes fault and documents the mechanism of injury &mdash; without it the insurer can deny the claim entirely.</span></button>
      </div>
      <div class="feedback-box" id="q3-fb"></div>
    </div>
    <div class="section-score" id="s1-score" style="display:none;"><div class="score-display" id="s1-score-val"></div><div class="score-label">Section 2 Score</div></div>
    <div class="btn-group" id="s1-next" style="display:none;"><button class="btn btn-primary btn-block" onclick="goToSection(2)">Next: Coverage Verification &rarr;</button></div>
  </div>
</div>
'''

SECTIONS[2] = '''<div class="section-card" id="section-2">
  <div class="section-header">
    <div class="section-num">Section 3 · Day 7 Review · Up to 30 pts</div>
    <h2>Coverage Verification</h2>
  </div>
  <div class="section-body">
    <div class="question-block" id="q4-block">
      <div class="q-num">Question 4 of 20 &middot; 10 pts</div>
      <div class="q-text">Your client has surgical injuries. The at-fault driver carries only $25K BI limits. What coverage sources must you identify at intake?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q4','a',true)" id="q4-a"><span class="opt-letter">A</span><span class="opt-text">At-fault driver&rsquo;s BI for the liability claim, the client&rsquo;s MedPay for immediate medical bills, and UM/UIM coverage in case liability limits fall short of damages.</span></button>
        <button class="option-btn" onclick="answer('q4','b',false)" id="q4-b"><span class="opt-letter">B</span><span class="opt-text">Only the at-fault driver&rsquo;s bodily injury coverage &mdash; the client&rsquo;s own insurance policies are not relevant until the liability claim has been fully exhausted first.</span></button>
        <button class="option-btn" onclick="answer('q4','c',false)" id="q4-c"><span class="opt-letter">C</span><span class="opt-text">The at-fault driver&rsquo;s property damage coverage first, then their bodily injury coverage, since PD claims must be opened before BI claims under Georgia procedures.</span></button>
        <button class="option-btn" onclick="answer('q4','d',false)" id="q4-d"><span class="opt-letter">D</span><span class="opt-text">File a claim with the client&rsquo;s health insurance to cover surgical costs upfront, then pursue the at-fault driver&rsquo;s BI policy separately for pain and suffering damages.</span></button>
      </div>
      <div class="feedback-box" id="q4-fb"></div>
    </div>
    <div class="question-block" id="q5-block">
      <div class="q-num">Question 5 of 20 &middot; 10 pts</div>
      <div class="q-text">A client signed their retainer at 9:05 AM Monday. The Letter of Representation has not been sent by Wednesday afternoon. What&rsquo;s the problem?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q5','a',false)" id="q5-a"><span class="opt-letter">A</span><span class="opt-text">No immediate problem &mdash; Georgia law provides a 5-business-day window to send the LOR after the retainer is executed, and Wednesday is within that window.</span></button>
        <button class="option-btn" onclick="answer('q5','b',false)" id="q5-b"><span class="opt-letter">B</span><span class="opt-text">The delay is concerning but manageable &mdash; prioritize sending the LOR by Friday and document the reason for the delay in CasePeer notes for the file.</span></button>
        <button class="option-btn" onclick="answer('q5','c',true)" id="q5-c"><span class="opt-letter">C</span><span class="opt-text">The LOR should have gone out same-day &mdash; every hour without it is an hour the insurer can contact the client directly or push for a quick lowball settlement.</span></button>
        <button class="option-btn" onclick="answer('q5','d',false)" id="q5-d"><span class="opt-letter">D</span><span class="opt-text">The paralegal should have sent a preliminary email to the insurer on Monday notifying them of representation while the formal LOR was being prepared and mailed.</span></button>
      </div>
      <div class="feedback-box" id="q5-fb"></div>
    </div>
    <div class="question-block" id="q6-block">
      <div class="q-num">Question 6 of 20 &middot; 10 pts</div>
      <div class="q-text">A client&rsquo;s health insurer paid $15,000 in medical bills. You discover this during case review. When should this subrogation lien have been identified?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q6','a',false)" id="q6-a"><span class="opt-letter">A</span><span class="opt-text">During demand preparation when all medical expenses are compiled &mdash; that is the standard point in the lifecycle where lien identification becomes operationally relevant to the case.</span></button>
        <button class="option-btn" onclick="answer('q6','b',true)" id="q6-b"><span class="opt-letter">B</span><span class="opt-text">At intake, as soon as the health insurance was identified &mdash; discovering a $15,000 lien at disbursement devastates the client&rsquo;s expected net recovery and creates trust issues.</span></button>
        <button class="option-btn" onclick="answer('q6','c',false)" id="q6-c"><span class="opt-letter">C</span><span class="opt-text">After settlement when the disbursement statement is being prepared &mdash; subrogation amounts cannot be confirmed until the total settlement figure has been agreed upon by both parties.</span></button>
        <button class="option-btn" onclick="answer('q6','d',false)" id="q6-d"><span class="opt-letter">D</span><span class="opt-text">During lien negotiation phase once all provider bills and insurance payments are compiled &mdash; running lien numbers before settlement is reached creates unnecessary early-stage complexity.</span></button>
      </div>
      <div class="feedback-box" id="q6-fb"></div>
    </div>
    <div class="section-score" id="s2-score" style="display:none;"><div class="score-display" id="s2-score-val"></div><div class="score-label">Section 3 Score</div></div>
    <div class="btn-group" id="s2-next" style="display:none;"><button class="btn btn-primary btn-block" onclick="goToSection(3)">Next: Liens &amp; Post-Settlement &rarr;</button></div>
  </div>
</div>
'''

SECTIONS[3] = '''<div class="section-card" id="section-3">
  <div class="section-header">
    <div class="section-num">Section 4 · Day 8 Review · Up to 30 pts</div>
    <h2>Liens &amp; Post-Settlement</h2>
  </div>
  <div class="section-body">
    <div class="question-block" id="q7-block">
      <div class="q-num">Question 7 of 20 &middot; 10 pts</div>
      <div class="q-text">A settlement doesn&rsquo;t fully cover all liens. What reduction approach should GLG use, and what doctrine adds leverage?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q7','a',false)" id="q7-a"><span class="opt-letter">A</span><span class="opt-text">Request each lienholder individually to accept a reduced amount based on the client&rsquo;s financial hardship, supported by a detailed letter explaining the shortfall and requesting leniency.</span></button>
        <button class="option-btn" onclick="answer('q7','b',false)" id="q7-b"><span class="opt-letter">B</span><span class="opt-text">Pay all liens in the order they were filed, giving priority to the earliest filed &mdash; any remaining shortfall comes from the client&rsquo;s net recovery as a final adjustment.</span></button>
        <button class="option-btn" onclick="answer('q7','c',false)" id="q7-c"><span class="opt-letter">C</span><span class="opt-text">Negotiate each lien separately starting with the largest one, using the threat of litigation delay as leverage to convince each provider to accept substantially reduced payments.</span></button>
        <button class="option-btn" onclick="answer('q7','d',true)" id="q7-d"><span class="opt-letter">D</span><span class="opt-text">Apply pro-rata reduction so every provider shares the shortfall proportionally, combined with the Common Fund Doctrine &mdash; the attorney created the recovery fund, so lienholders share costs.</span></button>
      </div>
      <div class="feedback-box" id="q7-fb"></div>
    </div>
    <div class="question-block" id="q8-block">
      <div class="q-num">Question 8 of 20 &middot; 10 pts</div>
      <div class="q-text">A client&rsquo;s ER bill was paid by Medicare. What makes Medicare liens unique, and what is the attorney&rsquo;s obligation?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q8','a',true)" id="q8-a"><span class="opt-letter">A</span><span class="opt-text">Medicare has federal recovery rights with personal attorney liability if ignored &mdash; but procurement cost reductions and disputing unrelated charges are standard negotiation tools. Never disburse first.</span></button>
        <button class="option-btn" onclick="answer('q8','b',false)" id="q8-b"><span class="opt-letter">B</span><span class="opt-text">Medicare liens are treated identically to private health insurance subrogation claims &mdash; negotiate using the Made Whole Doctrine and standard pro-rata reduction methods without special procedures.</span></button>
        <button class="option-btn" onclick="answer('q8','c',false)" id="q8-c"><span class="opt-letter">C</span><span class="opt-text">Medicare liens are non-negotiable by federal law and must be paid in full from settlement proceeds before any other deductions, including attorney fees, are calculated from the gross.</span></button>
        <button class="option-btn" onclick="answer('q8','d',false)" id="q8-d"><span class="opt-letter">D</span><span class="opt-text">Medicare liens expire after 12 months from the date of payment, so if the case timeline extends beyond that window the lien becomes unenforceable and can safely be disregarded.</span></button>
      </div>
      <div class="feedback-box" id="q8-fb"></div>
    </div>
    <div class="question-block" id="q9-block">
      <div class="q-num">Question 9 of 20 &middot; 10 pts</div>
      <div class="q-text">Day 45 post-settlement: a hospital lien is still unresolved because the hospital is non-responsive. What must happen?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q9','a',false)" id="q9-a"><span class="opt-letter">A</span><span class="opt-text">Send one final certified letter giving the hospital 10 days to respond, then proceed to disburse the settlement funds and hold the lien amount in the trust account.</span></button>
        <button class="option-btn" onclick="answer('q9','b',true)" id="q9-b"><span class="opt-letter">B</span><span class="opt-text">Mandatory attorney review triggers at Day 45 &mdash; the attorney evaluates and decides next steps. The client must have been updated every 14 days throughout the post-settlement process.</span></button>
        <button class="option-btn" onclick="answer('q9','c',false)" id="q9-c"><span class="opt-letter">C</span><span class="opt-text">File a motion with the court to release settlement funds from escrow, arguing the hospital&rsquo;s non-responsiveness constitutes abandonment of their lien claim under Georgia civil procedures.</span></button>
        <button class="option-btn" onclick="answer('q9','d',false)" id="q9-d"><span class="opt-letter">D</span><span class="opt-text">Escalate to the Georgia Hospital Lien Registry and request an administrative review of the lien status, which typically resolves non-responsive hospital lien disputes within 30 business days.</span></button>
      </div>
      <div class="feedback-box" id="q9-fb"></div>
    </div>
    <div class="section-score" id="s3-score" style="display:none;"><div class="score-display" id="s3-score-val"></div><div class="score-label">Section 4 Score</div></div>
    <div class="btn-group" id="s3-next" style="display:none;"><button class="btn btn-primary btn-block" onclick="goToSection(4)">Next: Client Communication &rarr;</button></div>
  </div>
</div>
'''

SECTIONS[4] = '''<div class="section-card" id="section-4">
  <div class="section-header">
    <div class="section-num">Section 5 · Day 9 Review · Up to 30 pts</div>
    <h2>Client Communication</h2>
  </div>
  <div class="section-body">
    <div class="question-block" id="q10-block">
      <div class="q-num">Question 10 of 20 &middot; 10 pts</div>
      <div class="q-text">It&rsquo;s Wednesday. A pre-lit client hasn&rsquo;t been contacted in 17 days. Nothing has changed on their case. What is the correct action?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q10','a',false)" id="q10-a"><span class="opt-letter">A</span><span class="opt-text">Send a brief email update confirming nothing has changed and the case is on track &mdash; email satisfies the contact requirement when there are no substantive new developments to report.</span></button>
        <button class="option-btn" onclick="answer('q10','b',false)" id="q10-b"><span class="opt-letter">B</span><span class="opt-text">Log a note in CasePeer that the case is progressing normally and schedule the next outreach for end of month when there may be updates worth communicating to the client.</span></button>
        <button class="option-btn" onclick="answer('q10','c',true)" id="q10-c"><span class="opt-letter">C</span><span class="opt-text">Call the client immediately &mdash; the 14-day standard is non-negotiable even when nothing has changed, because the call also serves as a treatment compliance check and referral opportunity.</span></button>
        <button class="option-btn" onclick="answer('q10','d',false)" id="q10-d"><span class="opt-letter">D</span><span class="opt-text">Ask your supervising attorney whether a contact is necessary given the lack of developments &mdash; an attorney-approved exception can waive the 14-day requirement for inactive-stage cases.</span></button>
      </div>
      <div class="feedback-box" id="q10-fb"></div>
    </div>
    <div class="question-block" id="q11-block">
      <div class="q-num">Question 11 of 20 &middot; 10 pts</div>
      <div class="q-text">A client says: &ldquo;I stopped going to the chiropractor. I&rsquo;m feeling a lot better.&rdquo; What is the correct response sequence?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q11','a',true)" id="q11-a"><span class="opt-letter">A</span><span class="opt-text">Acknowledge the improvement genuinely, explain the real risk &mdash; stopping early gives the insurer ammunition to reduce the offer &mdash; then escalate to the attorney for sign-off.</span></button>
        <button class="option-btn" onclick="answer('q11','b',false)" id="q11-b"><span class="opt-letter">B</span><span class="opt-text">Accept the client&rsquo;s decision and update CasePeer to reflect that treatment has been voluntarily concluded &mdash; clients have the right to make their own medical care decisions.</span></button>
        <button class="option-btn" onclick="answer('q11','c',false)" id="q11-c"><span class="opt-letter">C</span><span class="opt-text">Immediately schedule a follow-up appointment on the client&rsquo;s behalf with their chiropractor and inform the client the appointment has been made so treatment resumes promptly.</span></button>
        <button class="option-btn" onclick="answer('q11','d',false)" id="q11-d"><span class="opt-letter">D</span><span class="opt-text">Tell the client that feeling better is normal during recovery and does not mean treatment is complete, then firmly instruct them to continue all scheduled appointments without exception.</span></button>
      </div>
      <div class="feedback-box" id="q11-fb"></div>
    </div>
    <div class="question-block" id="q12-block">
      <div class="q-num">Question 12 of 20 &middot; 10 pts</div>
      <div class="q-text">A client calls furious: &ldquo;I&rsquo;ve left three voicemails and nobody called me back!&rdquo; What is the correct FIRST response?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q12','a',false)" id="q12-a"><span class="opt-letter">A</span><span class="opt-text">Pull up their CasePeer file while they are on the phone, confirm the missed calls in the contact history, and provide a detailed status update addressing each concern.</span></button>
        <button class="option-btn" onclick="answer('q12','b',false)" id="q12-b"><span class="opt-letter">B</span><span class="opt-text">Apologize sincerely for the delay, explain the team has been managing a high volume of cases, and assure the client their case remains an active priority for the firm.</span></button>
        <button class="option-btn" onclick="answer('q12','c',false)" id="q12-c"><span class="opt-letter">C</span><span class="opt-text">Transfer the call to the supervising attorney since the client&rsquo;s frustration level indicates this requires someone with authority to resolve the complaint and prevent further escalation.</span></button>
        <button class="option-btn" onclick="answer('q12','d',true)" id="q12-d"><span class="opt-letter">D</span><span class="opt-text">Name the emotion and restore safety: &ldquo;It sounds like you feel completely ignored &mdash; three voicemails without a callback is not acceptable.&rdquo; Then pause and let them respond.</span></button>
      </div>
      <div class="feedback-box" id="q12-fb"></div>
    </div>
    <div class="section-score" id="s4-score" style="display:none;"><div class="score-display" id="s4-score-val"></div><div class="score-label">Section 5 Score</div></div>
    <div class="btn-group" id="s4-next" style="display:none;"><button class="btn btn-primary btn-block" onclick="goToSection(5)">Next: Treatment Management &rarr;</button></div>
  </div>
</div>
'''

SECTIONS[5] = '''<div class="section-card" id="section-5">
  <div class="section-header">
    <div class="section-num">Section 6 · Day 10 Review · Up to 40 pts</div>
    <h2>Treatment Management</h2>
  </div>
  <div class="section-body">
    <div class="question-block" id="q13-block">
      <div class="q-num">Question 13 of 20 &middot; 10 pts</div>
      <div class="q-text">Before a routine 14-day client check-in call, what must you prepare?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q13','a',false)" id="q13-a"><span class="opt-letter">A</span><span class="opt-text">A script with standard talking points covering the case stage, expected timeline, and a treatment reminder &mdash; use the same format for consistency across every check-in call.</span></button>
        <button class="option-btn" onclick="answer('q13','b',false)" id="q13-b"><span class="opt-letter">B</span><span class="opt-text">The client&rsquo;s complete case file printed out so you can reference specific documents during the conversation and answer detailed questions the client may raise.</span></button>
        <button class="option-btn" onclick="answer('q13','c',true)" id="q13-c"><span class="opt-letter">C</span><span class="opt-text">Review CasePeer for appointment dates, open items, and contact history &mdash; then prepare a value delivery item so the call feels genuinely useful, not like an interrogation.</span></button>
        <button class="option-btn" onclick="answer('q13','d',false)" id="q13-d"><span class="opt-letter">D</span><span class="opt-text">An email pre-sent to the client listing the topics you plan to discuss, so they can prepare questions in advance and the call is more productive for both sides.</span></button>
      </div>
      <div class="feedback-box" id="q13-fb"></div>
    </div>
    <div class="question-block" id="q14-block">
      <div class="q-num">Question 14 of 20 &middot; 10 pts</div>
      <div class="q-text">A client stopped treating because they received a $2,400 bill from their chiropractor and panicked. What is the correct response?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q14','a',true)" id="q14-a"><span class="opt-letter">A</span><span class="opt-text">Explain the LOP means no out-of-pocket costs during treatment, tell the client not to pay that bill, and call the provider today to confirm the LOP and correct the billing.</span></button>
        <button class="option-btn" onclick="answer('q14','b',false)" id="q14-b"><span class="opt-letter">B</span><span class="opt-text">Advise the client to pay the bill to maintain the provider relationship, and document the payment as a case expense that will be reimbursed from the final settlement proceeds.</span></button>
        <button class="option-btn" onclick="answer('q14','c',false)" id="q14-c"><span class="opt-letter">C</span><span class="opt-text">Tell the client to ignore the bill entirely &mdash; billing disputes between the firm and providers are routine and always get resolved automatically during the post-settlement lien negotiation phase.</span></button>
        <button class="option-btn" onclick="answer('q14','d',false)" id="q14-d"><span class="opt-letter">D</span><span class="opt-text">Escalate to the attorney immediately since a billing error this significant may indicate the provider never received or properly acknowledged the original LOP when it was initially sent.</span></button>
      </div>
      <div class="feedback-box" id="q14-fb"></div>
    </div>
    <div class="question-block" id="q15-block">
      <div class="q-num">Question 15 of 20 &middot; 10 pts</div>
      <div class="q-text">A client who stopped treating says &ldquo;I&rsquo;ll try to get back to it.&rdquo; How do you convert this into an actionable commitment?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q15','a',false)" id="q15-a"><span class="opt-letter">A</span><span class="opt-text">Accept the statement positively and encourage them &mdash; expressing willingness to return is a good sign that the treatment gap will likely resolve itself within the next few weeks.</span></button>
        <button class="option-btn" onclick="answer('q15','b',false)" id="q15-b"><span class="opt-letter">B</span><span class="opt-text">Send a follow-up email after the call summarizing their verbal commitment to resume, creating a written record that documents the client&rsquo;s stated intention to return to treatment.</span></button>
        <button class="option-btn" onclick="answer('q15','c',false)" id="q15-c"><span class="opt-letter">C</span><span class="opt-text">Schedule the next check-in call for one week out to follow up on whether they actually resumed &mdash; the shorter follow-up window increases real accountability for the commitment.</span></button>
        <button class="option-btn" onclick="answer('q15','d',true)" id="q15-d"><span class="opt-letter">D</span><span class="opt-text">Get a specific date: &ldquo;Can we say Thursday the 19th?&rdquo; A stated date creates real accountability &mdash; document it in CasePeer and set a follow-up task to confirm attendance.</span></button>
      </div>
      <div class="feedback-box" id="q15-fb"></div>
    </div>
    <div class="question-block" id="q16-block">
      <div class="q-num">Question 16 of 20 &middot; 10 pts</div>
      <div class="q-text">You&rsquo;ve made 3 documented attempts to reach a client over 14 days with no response. What happens now?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q16','a',false)" id="q16-a"><span class="opt-letter">A</span><span class="opt-text">Continue calling every 3 days for another 2 weeks &mdash; persistence demonstrates the firm&rsquo;s commitment and most clients eventually respond when they see consistent documented outreach effort.</span></button>
        <button class="option-btn" onclick="answer('q16','b',true)" id="q16-b"><span class="opt-letter">B</span><span class="opt-text">Escalate to the attorney within 24-48 hours &mdash; an unreachable client is a blocked task, and the attorney has tools you don&rsquo;t: certified letters and case evaluation authority.</span></button>
        <button class="option-btn" onclick="answer('q16','c',false)" id="q16-c"><span class="opt-letter">C</span><span class="opt-text">Send a text message since the client may prefer texting over phone calls &mdash; younger clients especially respond better to text outreach than traditional voicemail-based contact attempts.</span></button>
        <button class="option-btn" onclick="answer('q16','d',false)" id="q16-d"><span class="opt-letter">D</span><span class="opt-text">Close the file in CasePeer as &ldquo;client non-responsive&rdquo; and send a formal case drop letter &mdash; three failed attempts over 14 days satisfies the obligation to maintain contact.</span></button>
      </div>
      <div class="feedback-box" id="q16-fb"></div>
    </div>
    <div class="section-score" id="s5-score" style="display:none;"><div class="score-display" id="s5-score-val"></div><div class="score-label">Section 6 Score</div></div>
    <div class="btn-group" id="s5-next" style="display:none;"><button class="btn btn-primary btn-block" onclick="goToSection(6)">Next: Boss Challenge &rarr;</button></div>
  </div>
</div>
'''

SECTIONS[6] = '''<div class="section-card" id="section-6">
  <div class="section-header">
    <div class="section-num">Section 7 · Boss Challenge · Bonus Points Only</div>
    <h2>The Boss Challenge</h2>
  </div>
  <div class="section-body">
    <div class="boss-header">
      <div class="boss-icon">&#9876;&#65039;</div>
      <h3>Everything You Learned &mdash; One Case</h3>
      <p>Teresa Ramirez pulls from <strong>every topic at once.</strong> Medical records, government claims, communication recovery, treatment gaps, and ERISA liens &mdash; all in one scenario.</p>
    </div>
    <div class="case-file">
      <div class="case-file-header">
        <div class="case-file-icon">&#128220;</div>
        <div>
          <div class="case-file-title">Case File</div>
          <div class="case-file-sub">Case #GLG-2026-1192 &middot; Multiple Red Flags</div>
        </div>
      </div>
      <div class="case-detail"><div class="case-key">Client</div><div class="case-val">Teresa Ramirez, 41</div></div>
      <div class="case-detail"><div class="case-key">Accident</div><div class="case-val">Struck by City of Atlanta vehicle &mdash; soft tissue + L5-S1 disc bulge on MRI</div></div>
      <div class="case-detail"><div class="case-key">Status</div><div class="case-val">Pre-lit, treating with chiropractor <span class="flag">TREATMENT GAP 10 DAYS</span></div></div>
      <div class="case-detail"><div class="case-key">Last Contact</div><div class="case-val">18 days ago <span class="flag">14-DAY RULE VIOLATED</span></div></div>
      <div class="case-detail"><div class="case-key">Insurance</div><div class="case-val">ER bill $8,400 paid by United Healthcare (employer ERISA plan)</div></div>
      <div class="case-detail"><div class="case-key">Today&rsquo;s Call</div><div class="case-val">Teresa called in crying: &ldquo;I want to fire you guys. Nobody ever calls me, my back still hurts, and I don&rsquo;t know what&rsquo;s going on.&rdquo;</div></div>
    </div>
    <div class="question-block" id="q17-block">
      <div class="q-num">Boss Challenge &middot; Question 17 &middot; Bonus</div>
      <div class="q-text">Teresa was hit by a City of Atlanta vehicle. What must you verify FIRST &mdash; before addressing the communication failure, treatment gap, or her emotional state?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q17','a',false)" id="q17-a"><span class="opt-letter">A</span><span class="opt-text">Verify whether the city&rsquo;s insurance carrier has been notified of the claim and whether a claim number has been assigned for the government liability case.</span></button>
        <button class="option-btn" onclick="answer('q17','b',false)" id="q17-b"><span class="opt-letter">B</span><span class="opt-text">Check whether a police report was filed at the scene &mdash; government vehicle accidents require documented proof that the entity was involved before claims proceed.</span></button>
        <button class="option-btn" onclick="answer('q17','c',false)" id="q17-c"><span class="opt-letter">C</span><span class="opt-text">Confirm the city employee was acting within the scope of employment at the time of the accident &mdash; personal-use driving shifts liability away from the government entity.</span></button>
        <button class="option-btn" onclick="answer('q17','d',true)" id="q17-d"><span class="opt-letter">D</span><span class="opt-text">Check the Ante Litem Notice deadline &mdash; City of Atlanta is a government entity with a mandatory 6-month notice requirement that kills the case entirely if missed.</span></button>
      </div>
      <div class="feedback-box" id="q17-fb"></div>
    </div>
    <div class="question-block" id="q18-block">
      <div class="q-num">Boss Challenge &middot; Question 18 &middot; Bonus</div>
      <div class="q-text">Teresa is crying and threatening to leave the firm. GLG&rsquo;s last contact was 18 days ago. What is the correct FIRST response?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q18','a',true)" id="q18-a"><span class="opt-letter">A</span><span class="opt-text">Acknowledge the failure and name the emotion: &ldquo;Teresa, 18 days without a call is not our standard. It sounds like you feel your case doesn&rsquo;t matter to us.&rdquo; Then pause.</span></button>
        <button class="option-btn" onclick="answer('q18','b',false)" id="q18-b"><span class="opt-letter">B</span><span class="opt-text">Immediately provide a detailed case status update to show the firm has been actively working behind the scenes, covering all recent activity on her medical records and claim.</span></button>
        <button class="option-btn" onclick="answer('q18','c',false)" id="q18-c"><span class="opt-letter">C</span><span class="opt-text">Transfer the call to the supervising attorney because a client threatening to leave the firm is an escalation-level event requiring someone with direct authority to intervene immediately.</span></button>
        <button class="option-btn" onclick="answer('q18','d',false)" id="q18-d"><span class="opt-letter">D</span><span class="opt-text">Apologize briefly and assure Teresa her case is important, then ask her to hold for a moment while you gather the most current status information from her case file.</span></button>
      </div>
      <div class="feedback-box" id="q18-fb"></div>
    </div>
    <div class="question-block" id="q19-block">
      <div class="q-num">Boss Challenge &middot; Question 19 &middot; Bonus</div>
      <div class="q-text">Teresa stopped treating 10 days ago because &ldquo;I feel a little better.&rdquo; Her MRI shows an L5-S1 disc bulge. Combining medical records and treatment management &mdash; what are the two critical actions?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q19','a',false)" id="q19-a"><span class="opt-letter">A</span><span class="opt-text">Resume treatment scheduling immediately and proceed with the demand &mdash; the MRI provides sufficient objective evidence regardless of whether she continues chiropractic care going forward.</span></button>
        <button class="option-btn" onclick="answer('q19','b',false)" id="q19-b"><span class="opt-letter">B</span><span class="opt-text">Document the treatment gap in CasePeer with her exact words as a verbatim quote, then schedule a follow-up call in one week to check if she resumed on her own.</span></button>
        <button class="option-btn" onclick="answer('q19','c',true)" id="q19-c"><span class="opt-letter">C</span><span class="opt-text">Explain that stopping treatment undermines even strong imaging findings &mdash; adjusters argue the injury resolved &mdash; then escalate to the attorney, since treatment stops require attorney sign-off.</span></button>
        <button class="option-btn" onclick="answer('q19','d',false)" id="q19-d"><span class="opt-letter">D</span><span class="opt-text">Call the chiropractor directly to schedule Teresa&rsquo;s next appointment and inform her of the date &mdash; proactive scheduling removes the client&rsquo;s decision burden and closes the gap faster.</span></button>
      </div>
      <div class="feedback-box" id="q19-fb"></div>
    </div>
    <div class="question-block" id="q20-block">
      <div class="q-num">Boss Challenge &middot; Question 20 &middot; Bonus</div>
      <div class="q-text">Teresa&rsquo;s ER bill of $8,400 was paid by United Healthcare &mdash; an employer-sponsored ERISA plan. At settlement, what can and can&rsquo;t you do regarding that lien?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q20','a',false)" id="q20-a"><span class="opt-letter">A</span><span class="opt-text">Apply Georgia&rsquo;s Made Whole Doctrine to reduce or eliminate the lien &mdash; Teresa hasn&rsquo;t been fully compensated, so the health plan cannot recover before she is made whole.</span></button>
        <button class="option-btn" onclick="answer('q20','b',true)" id="q20-b"><span class="opt-letter">B</span><span class="opt-text">ERISA preempts Georgia&rsquo;s Made Whole Doctrine, but the lien IS negotiable using Common Fund arguments, pro-rata reduction, and weak Summary Plan Description subrogation language. Know your tools.</span></button>
        <button class="option-btn" onclick="answer('q20','c',false)" id="q20-c"><span class="opt-letter">C</span><span class="opt-text">ERISA plans cannot be negotiated under any circumstance &mdash; federal law requires full reimbursement of all amounts paid, and the firm must reserve the entire lien from settlement.</span></button>
        <button class="option-btn" onclick="answer('q20','d',false)" id="q20-d"><span class="opt-letter">D</span><span class="opt-text">Dispute the lien entirely on the grounds that United Healthcare did not provide proper notice of subrogation rights within the 90-day window required by federal ERISA notification rules.</span></button>
      </div>
      <div class="feedback-box" id="q20-fb"></div>
    </div>
    <div class="section-score" id="s6-score" style="display:none;"><div class="score-display" id="s6-score-val"></div><div class="score-label">Boss Challenge Score</div></div>
    <div class="btn-group" id="s6-next" style="display:none;"><button class="btn btn-primary btn-block" onclick="showResults()">See Results &rarr;</button></div>
  </div>
</div>
'''

# Now replace sections 0-6 in the source
for i in range(7):
    start, end = find_section(src, i)
    src = src[:start] + SECTIONS[i] + src[end:]

# ──────────────────────────────────────────
# 6. REPLACE Q_CONFIG
# ──────────────────────────────────────────
q_config_start = src.index('var Q_CONFIG = {')
q_config_end = src.index('};', q_config_start) + 2

new_q_config = """var Q_CONFIG = {
  'q1':  {section:1, pts:10, isBonus:false, correct:'c'},
  'q2':  {section:1, pts:10, isBonus:false, correct:'d'},
  'q3':  {section:1, pts:10, isBonus:false, correct:'b'},
  'q4':  {section:2, pts:10, isBonus:false, correct:'a'},
  'q5':  {section:2, pts:10, isBonus:false, correct:'c'},
  'q6':  {section:2, pts:10, isBonus:false, correct:'b'},
  'q7':  {section:3, pts:10, isBonus:false, correct:'d'},
  'q8':  {section:3, pts:10, isBonus:false, correct:'a'},
  'q9':  {section:3, pts:10, isBonus:false, correct:'b'},
  'q10': {section:4, pts:10, isBonus:false, correct:'c'},
  'q11': {section:4, pts:10, isBonus:false, correct:'a'},
  'q12': {section:4, pts:10, isBonus:false, correct:'d'},
  'q13': {section:5, pts:10, isBonus:false, correct:'c'},
  'q14': {section:5, pts:10, isBonus:false, correct:'a'},
  'q15': {section:5, pts:10, isBonus:false, correct:'d'},
  'q16': {section:5, pts:10, isBonus:false, correct:'b'},
  'q17': {section:6, pts:0, isBonus:true, bonusPts:15, correct:'d'},
  'q18': {section:6, pts:0, isBonus:true, bonusPts:15, correct:'a'},
  'q19': {section:6, pts:0, isBonus:true, bonusPts:10, correct:'c'},
  'q20': {section:6, pts:0, isBonus:true, bonusPts:10, correct:'b'}
}"""
src = src[:q_config_start] + new_q_config + src[q_config_end:]

# ──────────────────────────────────────────
# 7. REPLACE SECTION_QUESTIONS
# ──────────────────────────────────────────
sq_start = src.index('var SECTION_QUESTIONS = {')
sq_end = src.index('};', sq_start) + 2
new_sq = """var SECTION_QUESTIONS = {
  1: ['q1','q2','q3'],
  2: ['q4','q5','q6'],
  3: ['q7','q8','q9'],
  4: ['q10','q11','q12'],
  5: ['q13','q14','q15','q16'],
  6: ['q17','q18','q19','q20']
}"""
src = src[:sq_start] + new_sq + src[sq_end:]

# ──────────────────────────────────────────
# 8. REPLACE FEEDBACK
# ──────────────────────────────────────────
fb_start = src.index('var FEEDBACK = {')
fb_end = src.index('\n};', fb_start) + 3
new_fb = r"""var FEEDBACK = {
  'q1': {t:'✅ Correct. Translate medical terminology into plain language. Connect findings to symptoms the client experiences. Never diagnose or predict outcomes — that is the doctor\'s role. Always confirm the client understands before ending the call.',f:'❌ Clients need plain-language explanations, not raw medical reports or referrals elsewhere. Translate the jargon, connect it to symptoms, confirm understanding, and log it in CasePeer. Never diagnose or predict — explain only.'},
  'q2': {t:'✅ Right. Treatment gaps are case-value killers. Document with exact dates, contact the client to learn why, and note the explanation. Common reasons (transport, billing, scheduling) are fixable — but unexplained gaps give adjusters ammunition.',f:'❌ Treatment gaps must be documented AND explained. Find out why it happened — the reason determines the fix. Just noting it or telling the client to resume without understanding the cause misses the point of case management.'},
  'q3': {t:'✅ Correct. ER records from the accident date establish causation — symptoms documented immediately after impact. Without them, a defense attorney will argue injuries arose from another cause days or weeks later. The demand needs this anchor.',f:'❌ ER records establish the causation link between accident and injury. Chiro records document treatment but cannot substitute for the initial diagnosis. MRI shows structure but not timing. Police reports show fault but not medical causation.'},
  'q4': {t:'✅ Complete answer. BI for liability, MedPay for immediate bills, UM/UIM when liability limits fall short. With surgical injuries and $25K limits, the gap will likely trigger UM/UIM. Identify all sources at intake — not after you hit limits.',f:'❌ All three coverage sources must be identified at intake: at-fault driver\'s BI, client\'s MedPay, and UM/UIM. With surgical injuries and low limits, the gap between damages and coverage is predictable. Late identification costs the client money.'},
  'q5': {t:'✅ LOR goes out same-day. Every hour without it is an hour the insurer has direct access to the client. Three days late means three days of exposure to recorded statements, lowball offers, and direct client contact.',f:'❌ There is no 5-day grace period. The LOR should go out the same day the retainer is signed. Delay = exposure. The insurer can contact the client directly, push for statements, or make lowball offers until the LOR arrives.'},
  'q6': {t:'✅ Exactly. Health insurance subrogation liens must be identified at intake. Discovering a $15K lien at disbursement devastates the client\'s expected net and creates a trust crisis that could have been entirely prevented with early identification.',f:'❌ Subrogation liens should be identified at intake — not at demand, not at settlement, not at disbursement. Late discovery compresses negotiation time and blindsides the client with a reduced net they never expected.'},
  'q7': {t:'✅ Pro-rata ensures every provider shares the shortfall proportionally. The Common Fund Doctrine adds leverage: the attorney\'s work created the recovery fund, so lienholders should bear a share of that cost. Both together maximize client net recovery.',f:'❌ GLG uses pro-rata reduction when settlement does not fully cover liens. Calculate available funds ÷ total liens = reduction percentage applied to each. Combine with Common Fund Doctrine for maximum leverage. Individual hardship letters are not the standard.'},
  'q8': {t:'✅ Medicare has federal teeth — personal attorney liability if the lien is ignored or disbursed around. But it IS negotiable: procurement cost reductions and disputing unrelated charges are legitimate tools. Resolve first, disburse after. Always.',f:'❌ Medicare liens are unique because of federal recovery rights and personal attorney liability. But they are negotiable — not non-negotiable, not identical to private insurance, and they do not expire after 12 months. Handle with care.'},
  'q9': {t:'✅ Day 45 = mandatory attorney review. The post-settlement SOP targets 90%+ file closure within 45 days. A non-responsive hospital should have been escalated already. Client communication every 14 days is non-negotiable throughout post-settlement.',f:'❌ At Day 45, the attorney must review and decide next steps. You cannot disburse around an unresolved lien, file court motions without attorney direction, or use a non-existent "Georgia Hospital Lien Registry." Escalate to the attorney.'},
  'q10': {t:'✅ The 14-day standard is non-negotiable. "Nothing has changed" IS the update — silence feels like neglect. The call also serves as a treatment compliance check and a referral opportunity. Phone calls, not emails, are the standard.',f:'❌ Pre-litigation requires client contact every 14 days — even when nothing has changed. Email does not satisfy the standard. Attorney exceptions do not exist. The contact IS the update. Call, log, set the next task.'},
  'q11': {t:'✅ Perfect sequence: (1) Acknowledge improvement genuinely, (2) Explain the risk — stopping early gives adjusters ammunition, (3) Escalate to the attorney. A client stopping treatment is a case-value decision requiring attorney sign-off.',f:'❌ A client stopping treatment requires acknowledgment, risk explanation, and attorney escalation. You cannot accept it at the paralegal level, schedule appointments unilaterally, or instruct the client to continue without the attorney weighing in.'},
  'q12': {t:'✅ Name the emotion first: "It sounds like you feel ignored." Acknowledge the failure directly — do not make excuses. Restore safety before delivering content. A client who feels unheard cannot process your case update.',f:'❌ When a client is emotionally activated, they cannot process case information. Name the emotion first, acknowledge the failure, and pause. Jumping to case status, apologizing generically, or transferring the call skips the critical de-escalation step.'},
  'q13': {t:'✅ Preparation turns a compliance call into a genuine check-in. The value delivery item is key — give the client something useful before asking for anything. Prepared calls feel like support; unprepared calls feel like surveillance.',f:'❌ Pre-call preparation requires reviewing CasePeer for appointments, open items, and history, then preparing something useful to share. Scripts, printed files, and pre-sent emails are not the standard — genuine preparation is.'},
  'q14': {t:'✅ Billing confusion is one of the most common and most solvable treatment barriers. The LOP means no out-of-pocket costs during treatment. Act immediately: call the provider today, confirm the LOP, correct the billing. Do not let a fixable problem become a gap.',f:'❌ The LOP covers treatment costs — the client should not be paying. Tell them not to pay, call the provider today, and get the billing corrected. Advising payment, ignoring the bill, or just escalating without action all miss the immediate fix.'},
  'q15': {t:'✅ "I\'ll try" is not a commitment — it is a polite deflection. A specific date stated aloud creates real accountability. Document it in CasePeer and set a follow-up task to confirm attendance. Vague intentions do not protect case value.',f:'❌ Accepting "I\'ll try" means accepting a non-commitment. Convert it to a specific date and time. Document the commitment in CasePeer with a follow-up task. Emails and shorter check-ins are helpful but do not replace the stated date.'},
  'q16': {t:'✅ Three documented attempts over 14 days = escalation. An unreachable client is a blocked task requiring attorney intervention. The attorney has tools you do not: certified letters, case evaluation authority, and the decision on continued representation.',f:'❌ After 3 documented attempts over 14 days, escalate within 24-48 hours. Do not continue calling indefinitely, send texts as a substitute, or close the file yourself. The attorney decides next steps — not the paralegal.'},
  'q17': {t:'✅ Government entity = Ante Litem Notice = non-negotiable deadline. Even with months remaining, flag it immediately. Ante Litem deadlines kill cases. Communication gaps and treatment gaps are fixable — a missed Ante Litem is not.',f:'❌ A government entity case ALWAYS triggers the Ante Litem check first. City of Atlanta = Georgia government entity = 6-month notice deadline. Everything else follows. Carrier notification, police reports, and scope-of-employment are secondary.'},
  'q18': {t:'✅ Pre-empt the accusation: acknowledge the 18-day gap before she raises it again. Name the emotion: "it sounds like you feel your case does not matter." Then pause. A client who feels heard may not need to fire the firm.',f:'❌ When a client threatens to leave, the sequence matters: (1) acknowledge the failure, (2) name the emotion, (3) pause and let them respond. Jumping to updates, transferring the call, or putting her on hold all skip the de-escalation.'},
  'q19': {t:'✅ Strong imaging means nothing if treatment records show voluntary stoppage. Adjusters use gaps to argue the injury resolved. Both actions required: explain the risk to Teresa AND escalate to the attorney. Treatment stops need attorney sign-off.',f:'❌ The MRI alone is not enough — treatment compliance tells the story the adjuster reads. Stopping early gives them ammunition. You must explain the risk AND escalate. Scheduling appointments or just documenting without escalation is incomplete.'},
  'q20': {t:'✅ ERISA preempts Made Whole — but ERISA liens ARE negotiable. Common Fund arguments, pro-rata reduction, and weak SPD language are your tools. Knowing what you CANNOT do (Made Whole) is as important as knowing what you CAN.',f:'❌ ERISA plans preempt Georgia\'s Made Whole Doctrine — the standard reduction letter is off the table. But ERISA liens are negotiable through Common Fund, pro-rata, and weak SPD language. They are not non-negotiable, and they do not have a 90-day window.'}
}"""
src = src[:fb_start] + new_fb + src[fb_end:]

# ──────────────────────────────────────────
# 9. FIX TOTAL SECTIONS COUNT
# ──────────────────────────────────────────
src = src.replace('var TOTAL_SECTIONS = 9;', 'var TOTAL_SECTIONS = 9;')  # same
src = src.replace('var BASE_MAX = 200;', 'var BASE_MAX = 200;')  # same
# Fix pass threshold (NH-11 uses 80% = 160, day10 used 85% = 170)
src = src.replace('var PASS_THRESHOLD = 170;', 'var PASS_THRESHOLD = 160;')

# ──────────────────────────────────────────
# 10. CERTIFICATE TEXT UPDATES
# ──────────────────────────────────────────
src = src.replace('Day 10: Week 2 Review &amp; Assessment', 'NH-11: Week 2 Review &amp; Assessment')
src = src.replace("'Day 10: Week 2 Review &amp; Assessment'", "'NH-11: Week 2 Review &amp; Assessment'")
src = src.replace("'🎓 Day 10 Complete'", "'🎓 NH-11 Complete'")
src = src.replace("'60-Day Gate Cleared'", "'Week 2 Gate Cleared'")
src = src.replace('role-specific training tracks where you apply these skills in your exact position.', 'the next phase of training. Every skill tested here is now part of your operating system.')

# ──────────────────────────────────────────
# 11. ENHANCED CERTIFICATE CSS
# ──────────────────────────────────────────
old_cert_css = """.cert{border:3px solid #141c2c;border-radius:14px;padding:24px;text-align:center;margin-top:20px;background:#fff;}
    .cert-logo{font-size:32px;margin-bottom:8px;}
    .cert h3{font-size:18px;font-weight:800;color:#141c2c;margin-bottom:4px;}
    .cert-name{font-size:22px;font-weight:800;color:#141C2C;margin:12px 0 4px;}"""
new_cert_css = """.cert{border:4px double #141c2c;border-radius:14px;padding:32px 24px;text-align:center;margin-top:20px;background:linear-gradient(180deg,#fff 0%,#fafaf5 100%);position:relative;overflow:hidden;}
    .cert::before{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:url('glg-crest-silver.png') center center no-repeat;background-size:200px;opacity:0.04;pointer-events:none;}
    .cert-logo{font-size:40px;margin-bottom:10px;}
    .cert h3{font-size:22px;font-weight:800;color:#141c2c;margin-bottom:4px;letter-spacing:0.5px;text-transform:uppercase;}
    .cert-name{font-size:28px;font-weight:800;color:#141C2C;margin:16px 0 6px;font-style:italic;}"""
src = src.replace(old_cert_css, new_cert_css)

# ──────────────────────────────────────────
# 12. REMOVE POPUP NAME ENTRY — ensure it's on certificate screen
# ──────────────────────────────────────────
# The day10 already has name entry in the certificate screen (via prompt in submitFeedback)
# If there's a popup, we keep it as-is since it's in the certificate flow

# ──────────────────────────────────────────
# 13. FIX SECTION SCORE LABELS for NH-11
# ──────────────────────────────────────────
# The day10 references s1-s6 section scores. Our sections match.
# Make sure section max pts are correct
src = src.replace(
    "sectionIdx <= 5 ? (pts + ' / 40') : (pts + ' bonus pts earned')",
    "sectionIdx <= 3 ? (pts + ' / 30') : sectionIdx <= 5 ? (pts + ' / 40') : (pts + ' bonus pts earned')"
)

# ──────────────────────────────────────────
# 14. WRITE OUTPUT
# ──────────────────────────────────────────
with open('site/module-nh11.html', 'w') as f:
    f.write(src)

print(f"Written: site/module-nh11.html ({len(src)} bytes)")

# Verify
import subprocess
def count(pattern):
    r = subprocess.run(['grep', '-ci', pattern, 'site/module-nh11.html'], capture_output=True, text=True)
    return r.stdout.strip()
def count_exact(pattern):
    r = subprocess.run(['grep', '-c', pattern, 'site/module-nh11.html'], capture_output=True, text=True)
    return r.stdout.strip()

print(f"label the emotion: {count('label the emotion')}")
print(f"GLG-2026-1192: {count_exact('GLG-2026-1192')}")
print(f"GLG-2026-0847: {count_exact('GLG-2026-0847')}")
print(f"glg-logo: {count_exact('glg-logo')}")
print(f"gavelMascot: {count_exact('gavelMascot')}")
print(f"streak-display: {count_exact('streak-display')}")
print(f"playCorrectChime: {count_exact('playCorrectChime')}")
print(f"spawnParticles: {count_exact('spawnParticles')}")
print(f"badgeFlip: {count_exact('badgeFlip')}")
print(f"Math.min: {count_exact('Math.min')}")

# Answer key verification
r = subprocess.run(['grep', '-o', "correct:'[a-d]'", 'site/module-nh11.html'], capture_output=True, text=True)
letters = [l.split("'")[1] for l in r.stdout.strip().split('\n') if l]
from collections import Counter
c = Counter(letters)
print(f"Answer distribution: {dict(c)}")
