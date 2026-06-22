#!/usr/bin/env python3
"""Build LA-1 from day10 polished chassis — Records Retrieval & Follow-Up."""
import re

with open('site/module-nh11.html', 'r') as f:
    src = f.read()

# ── 1. TITLE + MODULE ID ──
# Simple global replacements that work regardless of exact formatting
src = src.replace('LA-1 \u2014 Week 2 Review', 'LA-1 \u2014 Records Retrieval')  # already has LA-1 from NH-11 swap
src = src.replace('NH-11 \u2014 Week 2 Review', 'LA-1 \u2014 Records Retrieval')
src = src.replace('NH-11', 'LA-1')  # catch remaining NH-11 refs
src = src.replace("'nh11'", "'la1'")
src = src.replace('"nh11"', '"la1"')
src = src.replace('Week 2 Review &amp; Assessment', 'Records Retrieval &amp; Follow-Up')
src = src.replace('Week 2 Review & Assessment', 'Records Retrieval & Follow-Up')

src = src.replace(
    '<title>LA-1 — Week 2 Review &amp; Assessment | Gunn Law Group</title>',
    '<title>LA-1 — Records Retrieval &amp; Follow-Up | Gunn Law Group</title>'
)
src = src.replace("'day10'", "'la1'")
src = src.replace('"day10"', '"la1"')
src = src.replace("'NH-11 Week 2 Review & Assessment'", "'LA-1 Records Retrieval & Follow-Up'")
src = src.replace('"NH-11 Week 2 Review & Assessment"', '"LA-1 Records Retrieval & Follow-Up"')

# ── 2. MANIFEST ──
manifest_end = src.index('<!DOCTYPE html>')
new_manifest = """<!--
LA-1 — Records Retrieval & Follow-Up (Polished)
Built: June 17, 2026
Base: site/module-day10.html (Day 10 polished chassis)
Content: LA track Day 1 — records requests, provider types, follow-up, CasePeer documentation
Answer Key: A=5 B=5 C=5 D=5 (verified)
Distractor Parity: All options within 20% word count (verified)
Banned Terms: 0 hits (all banned terms verified zero)
Case Numbers: Marcus Thompson = GLG-2026-0731 (unique)
moduleId: la1
moduleName: LA-1 Records Retrieval & Follow-Up
CasePeer Stages: Treating, Pending Demand
Source SOPs: Legal_Assistant_SOP_PreLit.md, Communication_Logging_Standards.md, Hospital_Lien_Verification_Checklist.md
-->
"""
src = new_manifest + src[manifest_end:]

# ── 3. HEADER ──
src = src.replace(
    '<div class="day-badge">NH-11 · Week 2 Review</div>',
    '<div class="day-badge">LA Track · Day 1</div>'
)
src = src.replace(
    '<h1>NH-11 — Week 2 Review &amp; Assessment</h1>',
    '<h1>LA-1 — Records Retrieval &amp; Follow-Up</h1>'
)
src = src.replace(
    '<p>Gunn Law Group · Legal Assistant Training</p>',
    '<p>Gunn Law Group · Legal Assistant Track</p>'
)

# ── 4. NAV PILLS ──
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
  <button class="nav-pill" id="nav-1" onclick="goToSection(1)">2. Your Role</button>
  <button class="nav-pill" id="nav-2" onclick="goToSection(2)">3. Requests</button>
  <button class="nav-pill" id="nav-3" onclick="goToSection(3)">4. Providers</button>
  <button class="nav-pill" id="nav-4" onclick="goToSection(4)">5. Follow-Up</button>
  <button class="nav-pill" id="nav-5" onclick="goToSection(5)">6. CasePeer</button>
  <button class="nav-pill" id="nav-6" onclick="goToSection(6)">7. Boss</button>
  <button class="nav-pill" id="nav-7" onclick="goToSection(7)">8. Results</button>
  <button class="nav-pill" id="nav-8" onclick="goToSection(8)">9. Feedback</button>
</nav>'''
src = src.replace(old_nav, new_nav)

# ── 5. REPLACE SECTIONS ──
def find_section(html, section_id):
    marker = '<div class="section-card'
    pat = f'id="section-{section_id}"'
    idx = html.index(pat)
    start = html.rfind(marker, 0, idx)
    next_start = html.find(marker, idx + 1)
    if next_start == -1:
        next_start = html.find('</main>', idx)
    return start, next_start

SECTIONS = {}

SECTIONS[0] = '''<div class="section-card active" id="section-0">
  <div class="section-header">
    <div class="section-num">Section 1 · Welcome</div>
    <h2>Records Retrieval &amp; Follow-Up</h2>
    <div class="section-subhead">The foundation of every demand package starts here.</div>
  </div>
  <div class="section-body">
    <div class="scenario">
      <div class="scenario-tag">LA Track — Day 1</div>
      <h3>Every dollar in a demand package traces back to a medical record or a bill.</h3>
      <p>If a record is missing, the damages it represents are <span class="highlight">invisible to the adjuster.</span> Your job is to make sure <span class="urgent">nothing is invisible.</span></p>
    </div>
    <div class="info-block">
      <h4>&#128203; What You Will Learn</h4>
      <ul>
        <li>Your role as an LA in pre-litigation records retrieval</li>
        <li>How to identify <strong>every billing provider</strong> &mdash; not just the obvious ones</li>
        <li>The records request process: timelines, follow-up cadence, escalation</li>
        <li>CasePeer documentation standards for records tracking</li>
        <li>The &ldquo;damages on the table&rdquo; problem: what happens when you miss a provider</li>
      </ul>
    </div>
    <div class="callout callout-warn"><strong>Key principle:</strong> Records retrieval is consistently the #1 cause of demand backlog at the firm. The deadlines in this module are non-negotiable.</div>
    <div class="btn-group"><button class="btn btn-primary btn-block" onclick="goToSection(1)">Begin: Your Role as LA &rarr;</button></div>
  </div>
</div>
'''

SECTIONS[1] = '''<div class="section-card" id="section-1">
  <div class="section-header">
    <div class="section-num">Section 2 · Your Role · Up to 30 pts</div>
    <h2>The LA&rsquo;s Role in Records</h2>
  </div>
  <div class="section-body">
    <div class="info-block">
      <h4>&#128221; What You Own</h4>
      <p>As a Legal Assistant, you handle the administrative and tracking work so Case Managers can focus on client communication, case strategy, and demand quality. In records retrieval specifically:</p>
      <ul>
        <li>Submit medical records requests within <strong>48 hours</strong> of provider identification</li>
        <li>Follow up on all outstanding requests <strong>every 14 days</strong> &mdash; no exceptions</li>
        <li>Document every follow-up in CasePeer: date, method, result</li>
        <li>Report records outstanding over 30 days to your CM at weekly check-in</li>
        <li>Flag providers unresponsive after 3 follow-up attempts for paralegal escalation</li>
      </ul>
    </div>
    <div class="callout callout-danger"><strong>Core rule:</strong> You do NOT own cases. You do NOT communicate with clients &mdash; under any circumstances. If a client contacts you: take a message, log in CasePeer, notify the paralegal within 1 hour.</div>
    <div class="question-block" id="q1-block">
      <div class="q-num">Question 1 of 20 &middot; 10 pts</div>
      <div class="q-text">A client calls you directly asking about the status of their medical records. What is the correct response?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q1','a',false)" id="q1-a"><span class="opt-letter">A</span><span class="opt-text">Look up the records status in CasePeer and provide the client with a quick update since you have the information readily available.</span></button>
        <button class="option-btn" onclick="answer('q1','b',false)" id="q1-b"><span class="opt-letter">B</span><span class="opt-text">Transfer the call to the managing attorney since the client is reaching out to the wrong person and needs to be redirected by leadership.</span></button>
        <button class="option-btn" onclick="answer('q1','c',true)" id="q1-c"><span class="opt-letter">C</span><span class="opt-text">Say &ldquo;I will have your paralegal reach out shortly,&rdquo; log the contact in CasePeer immediately, and notify the paralegal within one hour.</span></button>
        <button class="option-btn" onclick="answer('q1','d',false)" id="q1-d"><span class="opt-letter">D</span><span class="opt-text">Ask the client to email their question instead so there is a written record, then forward the email to the paralegal for follow-up.</span></button>
      </div>
      <div class="feedback-box" id="q1-fb"></div>
    </div>
    <div class="question-block" id="q2-block">
      <div class="q-num">Question 2 of 20 &middot; 10 pts</div>
      <div class="q-text">A new provider is identified for a client&rsquo;s case on Monday morning. When must the records request be submitted?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q2','a',false)" id="q2-a"><span class="opt-letter">A</span><span class="opt-text">By the end of the current week, since batching records requests together for multiple providers is more efficient than sending them individually.</span></button>
        <button class="option-btn" onclick="answer('q2','b',false)" id="q2-b"><span class="opt-letter">B</span><span class="opt-text">Within 5 business days, which is the standard turnaround for administrative tasks that do not involve direct client communication or deadlines.</span></button>
        <button class="option-btn" onclick="answer('q2','c',false)" id="q2-c"><span class="opt-letter">C</span><span class="opt-text">Immediately that same day, before any other tasks, because records requests are always the single highest priority item on the LA task list.</span></button>
        <button class="option-btn" onclick="answer('q2','d',true)" id="q2-d"><span class="opt-letter">D</span><span class="opt-text">Within 48 hours of provider identification &mdash; by Wednesday morning at the latest. This deadline is non-negotiable per the LA performance standards.</span></button>
      </div>
      <div class="feedback-box" id="q2-fb"></div>
    </div>
    <div class="question-block" id="q3-block">
      <div class="q-num">Question 3 of 20 &middot; 10 pts</div>
      <div class="q-text">You realize you cannot complete a records task before its deadline. When should you notify your CM?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q3','a',false)" id="q3-a"><span class="opt-letter">A</span><span class="opt-text">At the weekly check-in meeting, since that is the designated time to discuss task status, blockers, and outstanding items with your supervising paralegal.</span></button>
        <button class="option-btn" onclick="answer('q3','b',true)" id="q3-b"><span class="opt-letter">B</span><span class="opt-text">Before the deadline passes &mdash; never after. Escalating early is never wrong, but sitting on a blocked task silently is a performance issue at this firm.</span></button>
        <button class="option-btn" onclick="answer('q3','c',false)" id="q3-c"><span class="opt-letter">C</span><span class="opt-text">After the deadline, with a written explanation of what went wrong. Documenting the reason for the delay is more important than giving advance notice.</span></button>
        <button class="option-btn" onclick="answer('q3','d',false)" id="q3-d"><span class="opt-letter">D</span><span class="opt-text">Only if the delay will exceed one full business week beyond the original deadline. Minor delays of a day or two are expected and do not require escalation.</span></button>
      </div>
      <div class="feedback-box" id="q3-fb"></div>
    </div>
    <div class="section-score" id="s1-score" style="display:none;"><div class="score-display" id="s1-score-val"></div><div class="score-label">Section 2 Score</div></div>
    <div class="btn-group" id="s1-next" style="display:none;"><button class="btn btn-primary btn-block" onclick="goToSection(2)">Next: Records Request Process &rarr;</button></div>
  </div>
</div>
'''

SECTIONS[2] = '''<div class="section-card" id="section-2">
  <div class="section-header">
    <div class="section-num">Section 3 · Request Process · Up to 30 pts</div>
    <h2>Records Request Process</h2>
  </div>
  <div class="section-body">
    <div class="info-block">
      <h4>&#128203; The Request Workflow</h4>
      <ul>
        <li><strong>Step 1:</strong> Confirm a valid HIPAA authorization is on file (patient name, DOB, provider, purpose, signature, date)</li>
        <li><strong>Step 2:</strong> Prepare the records request &mdash; specify the exact records needed (ER records, imaging, treatment notes, billing statements)</li>
        <li><strong>Step 3:</strong> Send via the provider&rsquo;s preferred method (fax, mail, patient portal) within <strong>48 hours</strong></li>
        <li><strong>Step 4:</strong> Log the request in CasePeer immediately: date sent, method, provider name, records type requested</li>
        <li><strong>Step 5:</strong> Set a 14-day follow-up task in CasePeer</li>
      </ul>
    </div>
    <div class="question-block" id="q4-block">
      <div class="q-num">Question 4 of 20 &middot; 10 pts</div>
      <div class="q-text">You&rsquo;re preparing a records request for a hospital visit. The HIPAA authorization on file lists the client&rsquo;s maiden name, but the hospital has the married name. What should you do?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q4','a',true)" id="q4-a"><span class="opt-letter">A</span><span class="opt-text">Flag the name discrepancy to the paralegal immediately &mdash; a mismatched HIPAA authorization may be rejected by the provider, delaying records retrieval.</span></button>
        <button class="option-btn" onclick="answer('q4','b',false)" id="q4-b"><span class="opt-letter">B</span><span class="opt-text">Send the request with the maiden name authorization and include a note explaining the client changed names &mdash; most providers will accept this.</span></button>
        <button class="option-btn" onclick="answer('q4','c',false)" id="q4-c"><span class="opt-letter">C</span><span class="opt-text">Correct the authorization yourself by updating the name in the document, since this is an administrative fix that does not require paralegal involvement.</span></button>
        <button class="option-btn" onclick="answer('q4','d',false)" id="q4-d"><span class="opt-letter">D</span><span class="opt-text">Send the request with both names listed in the cover letter and let the hospital decide which authorization they prefer to use for the release.</span></button>
      </div>
      <div class="feedback-box" id="q4-fb"></div>
    </div>
    <div class="question-block" id="q5-block">
      <div class="q-num">Question 5 of 20 &middot; 10 pts</div>
      <div class="q-text">When logging a records request in CasePeer, which elements must be included?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q5','a',false)" id="q5-a"><span class="opt-letter">A</span><span class="opt-text">Just the date sent and the provider name &mdash; additional detail can be added later when the records arrive and the file is updated with received documents.</span></button>
        <button class="option-btn" onclick="answer('q5','b',false)" id="q5-b"><span class="opt-letter">B</span><span class="opt-text">The provider name and a general note that records were requested, since the specific details are tracked in the request letter itself, not in CasePeer.</span></button>
        <button class="option-btn" onclick="answer('q5','c',true)" id="q5-c"><span class="opt-letter">C</span><span class="opt-text">Date sent, method used (fax/mail/portal), provider name, specific records type requested, and the 14-day follow-up task set. If it is not in CasePeer, it did not happen.</span></button>
        <button class="option-btn" onclick="answer('q5','d',false)" id="q5-d"><span class="opt-letter">D</span><span class="opt-text">The HIPAA authorization reference number, the provider&rsquo;s fax confirmation page, and a copy of the request letter uploaded to the case file in OneDrive.</span></button>
      </div>
      <div class="feedback-box" id="q5-fb"></div>
    </div>
    <div class="question-block" id="q6-block">
      <div class="q-num">Question 6 of 20 &middot; 10 pts</div>
      <div class="q-text">You receive records from a chiropractor. The first visit note is dated March 3, but the next note jumps to April 14 &mdash; a 6-week gap. What do you do?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q6','a',false)" id="q6-a"><span class="opt-letter">A</span><span class="opt-text">File the records as received &mdash; the chiropractor sent what they have, and any missing visits were likely cancelled by the client and do not require follow-up.</span></button>
        <button class="option-btn" onclick="answer('q6','b',true)" id="q6-b"><span class="opt-letter">B</span><span class="opt-text">Send a supplemental records request immediately for the missing dates, log the gap in CasePeer, and flag it to the paralegal &mdash; incomplete records weaken the demand.</span></button>
        <button class="option-btn" onclick="answer('q6','c',false)" id="q6-c"><span class="opt-letter">C</span><span class="opt-text">Contact the client directly to ask whether they actually attended appointments during the gap period, since they would know if visits were missed or rescheduled.</span></button>
        <button class="option-btn" onclick="answer('q6','d',false)" id="q6-d"><span class="opt-letter">D</span><span class="opt-text">Note the gap in CasePeer and wait until the demand preparation phase, when the paralegal will review all records and decide if supplemental requests are needed.</span></button>
      </div>
      <div class="feedback-box" id="q6-fb"></div>
    </div>
    <div class="section-score" id="s2-score" style="display:none;"><div class="score-display" id="s2-score-val"></div><div class="score-label">Section 3 Score</div></div>
    <div class="btn-group" id="s2-next" style="display:none;"><button class="btn btn-primary btn-block" onclick="goToSection(3)">Next: Provider Types &amp; Billing &rarr;</button></div>
  </div>
</div>
'''

SECTIONS[3] = '''<div class="section-card" id="section-3">
  <div class="section-header">
    <div class="section-num">Section 4 · Provider Types · Up to 30 pts</div>
    <h2>Provider Types &amp; Billing Entities</h2>
  </div>
  <div class="section-body">
    <div class="callout callout-danger"><strong>The #1 records mistake:</strong> Requesting records from &ldquo;the hospital&rdquo; and thinking you are done. A single ER visit can generate <strong>3-5 separate billing entities</strong> &mdash; each with its own records and its own bill. Missing one = missing recoverable damages.</div>
    <div class="info-block">
      <h4>&#127973; One ER Visit = Multiple Providers</h4>
      <ul>
        <li><strong>Hospital facility bill</strong> &mdash; the hospital itself (room, nursing, equipment)</li>
        <li><strong>ER physician group bill</strong> &mdash; the doctor who treated the patient (separate billing entity)</li>
        <li><strong>Radiology group bill</strong> &mdash; the radiologist who read the X-rays or CT (separate billing entity)</li>
        <li><strong>Imaging facility bill</strong> &mdash; the MRI or CT facility if outside the hospital</li>
        <li><strong>Ambulance / EMS bill</strong> &mdash; county or private ambulance service</li>
        <li><strong>Specialists</strong> &mdash; orthopedic, neurologist, pain management (each separate)</li>
        <li><strong>Physical therapy / chiropractic</strong> &mdash; each provider is a separate request</li>
        <li><strong>Urgent care / walk-in clinic</strong> &mdash; often missed if client went before the ER</li>
        <li><strong>Pharmacy</strong> &mdash; prescription records documenting medications prescribed for the injury</li>
      </ul>
    </div>
    <div class="question-block" id="q7-block">
      <div class="q-num">Question 7 of 20 &middot; 10 pts</div>
      <div class="q-text">A client was taken to Grady Memorial Hospital by ambulance after an accident. You request records from Grady. What providers are you still MISSING?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q7','a',false)" id="q7-a"><span class="opt-letter">A</span><span class="opt-text">No providers are missing &mdash; Grady&rsquo;s records include all treatment, imaging, physician notes, and billing from the emergency department visit.</span></button>
        <button class="option-btn" onclick="answer('q7','b',false)" id="q7-b"><span class="opt-letter">B</span><span class="opt-text">Only the ambulance service &mdash; the ER physician, radiology, and imaging are all included in the hospital facility records request automatically.</span></button>
        <button class="option-btn" onclick="answer('q7','c',false)" id="q7-c"><span class="opt-letter">C</span><span class="opt-text">Only the follow-up providers like chiropractor or physical therapist &mdash; all emergency department providers bill through the hospital system directly.</span></button>
        <button class="option-btn" onclick="answer('q7','d',true)" id="q7-d"><span class="opt-letter">D</span><span class="opt-text">At minimum: the ambulance/EMS service, the ER physician group, and the radiology group &mdash; each bills separately from the hospital facility itself.</span></button>
      </div>
      <div class="feedback-box" id="q7-fb"></div>
    </div>
    <div class="question-block" id="q8-block">
      <div class="q-num">Question 8 of 20 &middot; 10 pts</div>
      <div class="q-text">Why does missing a billing provider matter for the client&rsquo;s case value?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q8','a',true)" id="q8-a"><span class="opt-letter">A</span><span class="opt-text">Every missing bill is recoverable damages left off the demand &mdash; if the adjuster does not see the expense documented, they do not pay for it. Money left on the table.</span></button>
        <button class="option-btn" onclick="answer('q8','b',false)" id="q8-b"><span class="opt-letter">B</span><span class="opt-text">Missing providers only matter if the total medical bills exceed the insurance policy limits, since below-limits cases settle based on pain and suffering, not bill totals.</span></button>
        <button class="option-btn" onclick="answer('q8','c',false)" id="q8-c"><span class="opt-letter">C</span><span class="opt-text">It creates a bad impression with the adjuster but does not actually change the settlement amount, since adjusters evaluate damages independently from the demand package.</span></button>
        <button class="option-btn" onclick="answer('q8','d',false)" id="q8-d"><span class="opt-letter">D</span><span class="opt-text">Missing providers delay the demand but do not affect the final settlement number, since the attorney can add missing bills during the negotiation phase after the initial offer.</span></button>
      </div>
      <div class="feedback-box" id="q8-fb"></div>
    </div>
    <div class="question-block" id="q9-block">
      <div class="q-num">Question 9 of 20 &middot; 10 pts</div>
      <div class="q-text">You are reviewing a case file and notice the client saw an urgent care clinic the day before their ER visit. No records request has been sent. What do you do?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q9','a',false)" id="q9-a"><span class="opt-letter">A</span><span class="opt-text">Skip the urgent care records since the ER visit is more comprehensive and will contain the official diagnosis &mdash; the urgent care visit is redundant for the demand.</span></button>
        <button class="option-btn" onclick="answer('q9','b',true)" id="q9-b"><span class="opt-letter">B</span><span class="opt-text">Submit a records request within 48 hours, log it in CasePeer, and set the 14-day follow-up &mdash; the urgent care bill is a separate recoverable expense for the demand.</span></button>
        <button class="option-btn" onclick="answer('q9','c',false)" id="q9-c"><span class="opt-letter">C</span><span class="opt-text">Ask the client whether the urgent care visit was related to the accident before sending a request, since some pre-accident medical visits are not relevant to the claim.</span></button>
        <button class="option-btn" onclick="answer('q9','d',false)" id="q9-d"><span class="opt-letter">D</span><span class="opt-text">Note the urgent care visit in CasePeer and wait until the demand preparation phase to decide whether those records are needed for the package or not.</span></button>
      </div>
      <div class="feedback-box" id="q9-fb"></div>
    </div>
    <div class="section-score" id="s3-score" style="display:none;"><div class="score-display" id="s3-score-val"></div><div class="score-label">Section 4 Score</div></div>
    <div class="btn-group" id="s3-next" style="display:none;"><button class="btn btn-primary btn-block" onclick="goToSection(4)">Next: Follow-Up &amp; Escalation &rarr;</button></div>
  </div>
</div>
'''

SECTIONS[4] = '''<div class="section-card" id="section-4">
  <div class="section-header">
    <div class="section-num">Section 5 · Follow-Up · Up to 30 pts</div>
    <h2>Follow-Up &amp; Escalation</h2>
  </div>
  <div class="section-body">
    <div class="info-block">
      <h4>&#128197; The Follow-Up Ladder</h4>
      <ul>
        <li><strong>Day 14:</strong> First follow-up &mdash; call the provider, log the attempt in CasePeer (date, method, person spoken to, result)</li>
        <li><strong>Day 28:</strong> Second follow-up &mdash; try a different contact method or time of day. Log everything.</li>
        <li><strong>Day 30+:</strong> Report to CM at weekly check-in that records are outstanding over 30 days</li>
        <li><strong>After 3 attempts:</strong> Flag to paralegal for escalation &mdash; the provider may need an attorney letter or subpoena</li>
      </ul>
    </div>
    <div class="callout callout-info"><strong>Quality standard:</strong> &ldquo;Called provider&rdquo; is NOT sufficient. &ldquo;Called Dr. Smith&rsquo;s office at 2:14 PM; spoke with billing dept (Maria); records expected within 10 days&rdquo; IS sufficient.</div>
    <div class="question-block" id="q10-block">
      <div class="q-num">Question 10 of 20 &middot; 10 pts</div>
      <div class="q-text">It has been 16 days since you sent a records request. The provider has not responded. What is the correct action?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q10','a',false)" id="q10-a"><span class="opt-letter">A</span><span class="opt-text">Wait until Day 30 to follow up, since Georgia law gives providers 30 days to respond to records requests and following up earlier may seem pushy or inappropriate.</span></button>
        <button class="option-btn" onclick="answer('q10','b',false)" id="q10-b"><span class="opt-letter">B</span><span class="opt-text">Send a second written request by fax and wait another 14 days before making phone contact, since written communication creates a better paper trail for the file.</span></button>
        <button class="option-btn" onclick="answer('q10','c',true)" id="q10-c"><span class="opt-letter">C</span><span class="opt-text">Call the provider now &mdash; the 14-day follow-up was due on Day 14, so you are already 2 days late. Log the call with date, method, person contacted, and result in CasePeer.</span></button>
        <button class="option-btn" onclick="answer('q10','d',false)" id="q10-d"><span class="opt-letter">D</span><span class="opt-text">Email the paralegal to ask whether a follow-up is needed yet, since the provider may still be within their normal processing window for medical records requests.</span></button>
      </div>
      <div class="feedback-box" id="q10-fb"></div>
    </div>
    <div class="question-block" id="q11-block">
      <div class="q-num">Question 11 of 20 &middot; 10 pts</div>
      <div class="q-text">You have made 3 follow-up attempts to a provider over 42 days. No response. What is the next step?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q11','a',true)" id="q11-a"><span class="opt-letter">A</span><span class="opt-text">Flag the provider to the paralegal for escalation immediately &mdash; after 3 documented attempts, the case may need an attorney demand letter or subpoena to get records.</span></button>
        <button class="option-btn" onclick="answer('q11','b',false)" id="q11-b"><span class="opt-letter">B</span><span class="opt-text">Continue calling every 7 days and documenting each attempt &mdash; persistence eventually works, and most providers respond before the case reaches the demand stage.</span></button>
        <button class="option-btn" onclick="answer('q11','c',false)" id="q11-c"><span class="opt-letter">C</span><span class="opt-text">Send a certified letter directly to the provider&rsquo;s compliance department threatening legal action if records are not produced within 10 business days of receipt.</span></button>
        <button class="option-btn" onclick="answer('q11','d',false)" id="q11-d"><span class="opt-letter">D</span><span class="opt-text">Move on and note in CasePeer that records are unavailable from this provider &mdash; the demand can proceed without them if other medical evidence is sufficient.</span></button>
      </div>
      <div class="feedback-box" id="q11-fb"></div>
    </div>
    <div class="question-block" id="q12-block">
      <div class="q-num">Question 12 of 20 &middot; 10 pts</div>
      <div class="q-text">You log a provider follow-up in CasePeer as: &ldquo;Called about records. No answer.&rdquo; What is wrong with this note?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q12','a',false)" id="q12-a"><span class="opt-letter">A</span><span class="opt-text">Nothing is wrong &mdash; recording the attempt and the result (no answer) is sufficient documentation for a follow-up call that did not connect with anyone.</span></button>
        <button class="option-btn" onclick="answer('q12','b',false)" id="q12-b"><span class="opt-letter">B</span><span class="opt-text">The note should include the client&rsquo;s name and case number so anyone reading it can identify which case the call was for without checking the case file header.</span></button>
        <button class="option-btn" onclick="answer('q12','c',false)" id="q12-c"><span class="opt-letter">C</span><span class="opt-text">The note should state which records you were calling about but does not need to include the specific time, phone number, or next steps for the follow-up attempt.</span></button>
        <button class="option-btn" onclick="answer('q12','d',true)" id="q12-d"><span class="opt-letter">D</span><span class="opt-text">Missing date, time, provider name, phone number called, specific records requested, and next action with deadline. &ldquo;Called about records&rdquo; fails the documentation quality standard.</span></button>
      </div>
      <div class="feedback-box" id="q12-fb"></div>
    </div>
    <div class="section-score" id="s4-score" style="display:none;"><div class="score-display" id="s4-score-val"></div><div class="score-label">Section 5 Score</div></div>
    <div class="btn-group" id="s4-next" style="display:none;"><button class="btn btn-primary btn-block" onclick="goToSection(5)">Next: CasePeer Documentation &rarr;</button></div>
  </div>
</div>
'''

SECTIONS[5] = '''<div class="section-card" id="section-5">
  <div class="section-header">
    <div class="section-num">Section 6 · CasePeer · Up to 40 pts</div>
    <h2>CasePeer Documentation</h2>
  </div>
  <div class="section-body">
    <div class="callout callout-warn"><strong>If it is not in CasePeer, it did not happen.</strong> This is the system of record. Every task completion, every follow-up, every document received &mdash; logged immediately, before moving to the next task.</div>
    <div class="question-block" id="q13-block">
      <div class="q-num">Question 13 of 20 &middot; 10 pts</div>
      <div class="q-text">You receive a batch of medical records by fax at 3:45 PM. When should you upload them to OneDrive and log receipt in CasePeer?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q13','a',false)" id="q13-a"><span class="opt-letter">A</span><span class="opt-text">First thing tomorrow morning, when you can review the records thoroughly and ensure they are complete before uploading and logging them in the case management system.</span></button>
        <button class="option-btn" onclick="answer('q13','b',false)" id="q13-b"><span class="opt-letter">B</span><span class="opt-text">Within 48 hours of receipt, matching the same timeline standard used for submitting outbound records requests to maintain consistency across documentation tasks.</span></button>
        <button class="option-btn" onclick="answer('q13','c',true)" id="q13-c"><span class="opt-letter">C</span><span class="opt-text">Same business day &mdash; upload to the case OneDrive folder, log receipt in CasePeer with date and provider, and update the case status fields before leaving for the day.</span></button>
        <button class="option-btn" onclick="answer('q13','d',false)" id="q13-d"><span class="opt-letter">D</span><span class="opt-text">After the paralegal reviews and confirms the records are complete &mdash; uploading incomplete records creates confusion about what the firm actually has on file for the case.</span></button>
      </div>
      <div class="feedback-box" id="q13-fb"></div>
    </div>
    <div class="question-block" id="q14-block">
      <div class="q-num">Question 14 of 20 &middot; 10 pts</div>
      <div class="q-text">You paid $35.00 for medical records from an imaging center. What must you do with the expense?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q14','a',true)" id="q14-a"><span class="opt-letter">A</span><span class="opt-text">Enter the $35 in CasePeer&rsquo;s Costs section immediately, save the receipt to the case OneDrive folder the same day. Retroactive tracking is a compliance failure.</span></button>
        <button class="option-btn" onclick="answer('q14','b',false)" id="q14-b"><span class="opt-letter">B</span><span class="opt-text">Keep the receipt and submit it at the end of the month with all other case expenses in a single batch &mdash; this is more efficient than individual daily entries.</span></button>
        <button class="option-btn" onclick="answer('q14','c',false)" id="q14-c"><span class="opt-letter">C</span><span class="opt-text">Forward the receipt to the accounting department, since case expenses are tracked centrally and do not need to be entered in CasePeer by the LA who incurred them.</span></button>
        <button class="option-btn" onclick="answer('q14','d',false)" id="q14-d"><span class="opt-letter">D</span><span class="opt-text">Log the expense in CasePeer when the records actually arrive, since recording the cost before receiving the records could create a discrepancy if the provider refunds.</span></button>
      </div>
      <div class="feedback-box" id="q14-fb"></div>
    </div>
    <div class="question-block" id="q15-block">
      <div class="q-num">Question 15 of 20 &middot; 10 pts</div>
      <div class="q-text">When you confirm your CM assigned you a task in CasePeer, what is the acknowledgment deadline?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q15','a',false)" id="q15-a"><span class="opt-letter">A</span><span class="opt-text">By the end of the business day, since checking CasePeer tasks once daily during morning dashboard review is the standard workflow for legal assistant task management.</span></button>
        <button class="option-btn" onclick="answer('q15','b',false)" id="q15-b"><span class="opt-letter">B</span><span class="opt-text">Within 24 hours of assignment, which gives you time to review the task requirements and assess whether you can complete it within the requested timeframe.</span></button>
        <button class="option-btn" onclick="answer('q15','c',false)" id="q15-c"><span class="opt-letter">C</span><span class="opt-text">Immediately upon seeing it &mdash; the LA should be monitoring CasePeer continuously and acknowledge every new task the moment it appears in the task queue.</span></button>
        <button class="option-btn" onclick="answer('q15','d',true)" id="q15-d"><span class="opt-letter">D</span><span class="opt-text">Within 4 hours of assignment. If you cannot meet the deadline, notify the CM before the deadline passes. This is the accountability system, not micromanagement.</span></button>
      </div>
      <div class="feedback-box" id="q15-fb"></div>
    </div>
    <div class="question-block" id="q16-block">
      <div class="q-num">Question 16 of 20 &middot; 10 pts</div>
      <div class="q-text">Your CasePeer data accuracy is audited at 91%. The performance standard is 95%. What is the consequence?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q16','a',false)" id="q16-a"><span class="opt-letter">A</span><span class="opt-text">No consequence &mdash; 91% is close enough to the target that it falls within an acceptable margin of error and does not trigger any performance review action.</span></button>
        <button class="option-btn" onclick="answer('q16','b',true)" id="q16-b"><span class="opt-letter">B</span><span class="opt-text">A performance conversation with your supervisor. Two occurrences of below-95% accuracy within 60 days escalates to reassignment or contract discontinuation. Fix it now.</span></button>
        <button class="option-btn" onclick="answer('q16','c',false)" id="q16-c"><span class="opt-letter">C</span><span class="opt-text">You receive additional training on CasePeer data entry procedures and are re-tested after 30 days, with no impact on your performance record unless you fail again.</span></button>
        <button class="option-btn" onclick="answer('q16','d',false)" id="q16-d"><span class="opt-letter">D</span><span class="opt-text">A note is added to your monthly scorecard but no immediate action is taken, since performance evaluations only happen during the quarterly review cycle with leadership.</span></button>
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
      <h3>Everything You Learned &mdash; One Case File</h3>
      <p>Records retrieval, provider identification, follow-up, documentation &mdash; all at once.</p>
    </div>
    <div class="case-file">
      <div class="case-file-header">
        <div class="case-file-icon">&#128220;</div>
        <div>
          <div class="case-file-title">Case File</div>
          <div class="case-file-sub">Case #GLG-2026-0731 &middot; Records Crisis</div>
        </div>
      </div>
      <div class="case-detail"><div class="case-key">Client</div><div class="case-val">Marcus Thompson, 29</div></div>
      <div class="case-detail"><div class="case-key">Accident</div><div class="case-val">T-bone collision at intersection. Ambulance to Grady ER. MRI at Peachtree Imaging two weeks later.</div></div>
      <div class="case-detail"><div class="case-key">Treatment</div><div class="case-val">Chiropractic 3x/week (Decatur Spine), orthopedic consult (Dr. Patel), PT at ATL Rehab</div></div>
      <div class="case-detail"><div class="case-key">Status</div><div class="case-val">Pending Demand &mdash; paralegal says &ldquo;demand is ready to go&rdquo; <span class="flag">RECORDS AUDIT NEEDED</span></div></div>
      <div class="case-detail"><div class="case-key">Your Task</div><div class="case-val">You pull the case file and discover records have only been requested from <strong>Grady Hospital</strong> and <strong>Decatur Spine</strong>. Nothing else.</div></div>
    </div>
    <div class="question-block" id="q17-block">
      <div class="q-num">Boss Challenge &middot; Question 17 &middot; Bonus</div>
      <div class="q-text">Looking at Marcus&rsquo;s case, how many billing providers are MISSING records requests? List the categories.</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q17','a',false)" id="q17-a"><span class="opt-letter">A</span><span class="opt-text">Two providers missing: Peachtree Imaging for the MRI and ATL Rehab for PT. The ER physician and radiology are included in Grady&rsquo;s hospital records package.</span></button>
        <button class="option-btn" onclick="answer('q17','b',false)" id="q17-b"><span class="opt-letter">B</span><span class="opt-text">Three providers missing: ambulance, Peachtree Imaging, and Dr. Patel&rsquo;s orthopedic office. ATL Rehab is optional since PT records add minimal demand value.</span></button>
        <button class="option-btn" onclick="answer('q17','c',false)" id="q17-c"><span class="opt-letter">C</span><span class="opt-text">Four providers missing: the ER physician group, Peachtree Imaging, Dr. Patel, and ATL Rehab. Ambulance records are typically not needed for the demand package.</span></button>
        <button class="option-btn" onclick="answer('q17','d',true)" id="q17-d"><span class="opt-letter">D</span><span class="opt-text">At least five: ambulance/EMS, ER physician group (separate from Grady facility), Grady radiology group, Peachtree Imaging, Dr. Patel orthopedic, and ATL Rehab PT.</span></button>
      </div>
      <div class="feedback-box" id="q17-fb"></div>
    </div>
    <div class="question-block" id="q18-block">
      <div class="q-num">Boss Challenge &middot; Question 18 &middot; Bonus</div>
      <div class="q-text">The paralegal says the demand is &ldquo;ready to go.&rdquo; You have just identified 5+ missing providers. What do you do?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q18','a',true)" id="q18-a"><span class="opt-letter">A</span><span class="opt-text">Flag the missing providers to the paralegal immediately with the specific list. The demand cannot go out without these records &mdash; each missing bill is damages left off the table.</span></button>
        <button class="option-btn" onclick="answer('q18','b',false)" id="q18-b"><span class="opt-letter">B</span><span class="opt-text">Send out all 5 records requests yourself first, then notify the paralegal once you have confirmation the requests are in process so you can report a solution, not a problem.</span></button>
        <button class="option-btn" onclick="answer('q18','c',false)" id="q18-c"><span class="opt-letter">C</span><span class="opt-text">Let the demand go out as planned and send supplemental records requests in parallel &mdash; the attorney can add the missing bills during negotiation if the records arrive in time.</span></button>
        <button class="option-btn" onclick="answer('q18','d',false)" id="q18-d"><span class="opt-letter">D</span><span class="opt-text">Ask the paralegal whether these additional providers are really necessary for the demand, since the existing Grady and chiropractic records may provide sufficient medical documentation.</span></button>
      </div>
      <div class="feedback-box" id="q18-fb"></div>
    </div>
    <div class="question-block" id="q19-block">
      <div class="q-num">Boss Challenge &middot; Question 19 &middot; Bonus</div>
      <div class="q-text">The paralegal agrees to hold the demand. You now need to request records from all 5+ missing providers. What is the correct prioritization?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q19','a',false)" id="q19-a"><span class="opt-letter">A</span><span class="opt-text">Start with the largest expected bill (Grady ER physician) and work down to the smallest, since higher-value records have the most impact on the demand total.</span></button>
        <button class="option-btn" onclick="answer('q19','b',false)" id="q19-b"><span class="opt-letter">B</span><span class="opt-text">Send one request per day over the next week to avoid overwhelming the providers and to allow you to track each request individually as it processes.</span></button>
        <button class="option-btn" onclick="answer('q19','c',true)" id="q19-c"><span class="opt-letter">C</span><span class="opt-text">All requests go out simultaneously today &mdash; every day of delay extends the demand hold. Set 14-day follow-up tasks for each provider. Log all requests in CasePeer immediately.</span></button>
        <button class="option-btn" onclick="answer('q19','d',false)" id="q19-d"><span class="opt-letter">D</span><span class="opt-text">Request the ER physician and radiology groups first since those are most commonly missed, then send the remaining requests after the first batch is confirmed received.</span></button>
      </div>
      <div class="feedback-box" id="q19-fb"></div>
    </div>
    <div class="question-block" id="q20-block">
      <div class="q-num">Boss Challenge &middot; Question 20 &middot; Bonus</div>
      <div class="q-text">Two weeks later, 4 of 5 providers have responded. ATL Rehab (PT) has not. This is their second non-response. You have one more attempt before escalation. What do you do?</div>
      <div class="options">
        <button class="option-btn" onclick="answer('q20','a',false)" id="q20-a"><span class="opt-letter">A</span><span class="opt-text">Send another fax request with a cover letter marked &ldquo;URGENT &mdash; SECOND REQUEST&rdquo; and set a 7-day follow-up, since written communication creates the strongest paper trail.</span></button>
        <button class="option-btn" onclick="answer('q20','b',true)" id="q20-b"><span class="opt-letter">B</span><span class="opt-text">Call ATL Rehab at a different time of day than previous attempts, speak with a specific person in billing, document the conversation in CasePeer with name, time, and outcome.</span></button>
        <button class="option-btn" onclick="answer('q20','c',false)" id="q20-c"><span class="opt-letter">C</span><span class="opt-text">Escalate directly to the paralegal now without making the third attempt &mdash; two non-responses from the same provider is already enough to justify attorney intervention.</span></button>
        <button class="option-btn" onclick="answer('q20','d',false)" id="q20-d"><span class="opt-letter">D</span><span class="opt-text">Visit ATL Rehab in person with the signed HIPAA authorization and request the records directly from their front desk, since in-person requests cannot be ignored or delayed.</span></button>
      </div>
      <div class="feedback-box" id="q20-fb"></div>
    </div>
    <div class="section-score" id="s6-score" style="display:none;"><div class="score-display" id="s6-score-val"></div><div class="score-label">Boss Challenge Score</div></div>
    <div class="btn-group" id="s6-next" style="display:none;"><button class="btn btn-primary btn-block" onclick="showResults()">See Results &rarr;</button></div>
  </div>
</div>
'''

for i in range(7):
    start, end = find_section(src, i)
    src = src[:start] + SECTIONS[i] + src[end:]

# ── 6. Q_CONFIG ──
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

# ── 7. SECTION_QUESTIONS ──
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

# ── 8. FEEDBACK ──
fb_start = src.index('var FEEDBACK = {')
fb_end = src.index('\n};', fb_start) + 3
new_fb = r"""var FEEDBACK = {
  'q1': {t:'✅ Correct. LAs do NOT communicate with clients — period. Take the message, log in CasePeer, notify the paralegal within 1 hour. No exceptions, no matter how simple the question seems.',f:'❌ LAs never provide case information to clients, not even records status. Say "I\'ll have your paralegal reach out shortly." Log it. Notify the paralegal. That is the complete procedure.'},
  'q2': {t:'✅ Within 48 hours of provider identification — non-negotiable. Records retrieval is the #1 cause of demand backlog. Every day of delay here delays the demand downstream.',f:'❌ The deadline is 48 hours from provider identification. Not end of week, not 5 days, not "immediately before everything else." 48 hours. Track it. Hit it. Every time.'},
  'q3': {t:'✅ Before the deadline — never after. Escalating early is always the right call. Sitting on a blocked task silently is what creates missed deadlines and trust failures.',f:'❌ Notify your CM BEFORE the deadline passes. Not at the weekly check-in, not after the deadline with an explanation, not only if the delay is long. Before. Always before.'},
  'q4': {t:'✅ Name discrepancies on HIPAA authorizations are a common rejection reason. Flag it immediately — the paralegal needs to get a corrected authorization before you can send the request.',f:'❌ A mismatched name on the HIPAA authorization will get your request rejected. You cannot correct it yourself (legal document), and sending it with a note is not reliable. Flag to paralegal.'},
  'q5': {t:'✅ Complete documentation: date, method, provider, records type, and the follow-up task. "If it is not in CasePeer, it did not happen." This is the firm\'s quality standard.',f:'❌ Partial logging creates gaps. The full entry requires: date sent, method (fax/mail/portal), provider name, specific records type requested, and the 14-day follow-up task. Every element matters.'},
  'q6': {t:'✅ A 6-week gap in treatment records could mean missing visits, incomplete records, or a treatment gap that needs explanation. Request supplemental records immediately and flag to the paralegal.',f:'❌ Never assume gaps in records are intentional or unimportant. Missing treatment notes weaken the demand. Send a supplemental request immediately, log the gap, and flag it — do not wait for demand prep.'},
  'q7': {t:'✅ One ER visit generates multiple separate billing entities. The ambulance, ER physician group, and radiology group each bill independently from the hospital facility. Missing any one = missing damages.',f:'❌ Hospital facility records do NOT include the ER physician group, radiology group, or ambulance/EMS. Each is a separate billing entity requiring its own records request. This is the #1 records mistake.'},
  'q8': {t:'✅ Every missing bill is money left off the demand. Adjusters pay what they see documented. If the ER physician group bill is not in the demand package, those damages are invisible.',f:'❌ Missing providers directly reduce settlement value. Adjusters evaluate damages based on documented medical expenses. An undocumented $2,000 radiology bill means $2,000 less in the demand.'},
  'q9': {t:'✅ Every provider visit related to the accident needs records and billing — including urgent care. The bill is a separate recoverable expense, and the records may document early symptoms.',f:'❌ Urgent care records are not redundant with the ER. They document a separate visit, generate a separate bill, and may show early symptoms. Request within 48 hours, log it, set follow-up.'},
  'q10': {t:'✅ The 14-day follow-up was due on Day 14. At Day 16 you are already late. Call now, document the call properly (date, time, person, result), and set the next follow-up task.',f:'❌ The 14-day follow-up is the firm\'s internal standard — do not wait for the provider\'s 30-day legal window. You are already 2 days past due. Call now and document properly.'},
  'q11': {t:'✅ Three documented attempts = escalation. The paralegal has tools you do not: attorney demand letters, subpoenas, direct provider relationships. Your job is to document and escalate on time.',f:'❌ After 3 documented attempts, escalate to the paralegal. Do not continue indefinitely, send threatening letters yourself, or give up. Escalation is the correct next step — that is why the procedure exists.'},
  'q12': {t:'✅ "Called about records. No answer." fails every quality standard. A proper note includes: date, time, provider name, phone number, specific records requested, and next action with deadline.',f:'❌ The quality standard is specific: who, when, what number, what records, what happened, what is next. "Called about records" would fail an audit and provides zero value to anyone reading the file.'},
  'q13': {t:'✅ Same business day. Upload to OneDrive, log in CasePeer, update status fields — all before leaving for the day. Tomorrow morning is already late by the firm\'s documentation standard.',f:'❌ Document upload and CasePeer logging must happen same business day. Not tomorrow, not within 48 hours, not after paralegal review. Same day. The file must always reflect current reality.'},
  'q14': {t:'✅ Enter the expense in CasePeer\'s Costs section immediately and save the receipt to OneDrive same day. Retroactive tracking is a compliance failure and creates disbursement problems downstream.',f:'❌ Case expenses are logged at the time incurred — not batched monthly, not forwarded to accounting, not delayed until records arrive. CasePeer Costs section + OneDrive receipt, same day.'},
  'q15': {t:'✅ 4 hours. This is the accountability system. If you cannot meet the task deadline, notify the CM before it passes. The acknowledgment confirms you received the assignment and accepted the timeline.',f:'❌ Task acknowledgment is within 4 hours — not end of day, not 24 hours, not immediately. 4 hours. If you cannot meet the deadline, say so before the deadline. That is the system.'},
  'q16': {t:'✅ Below 95% accuracy triggers a performance conversation. Two occurrences within 60 days = reassignment or contract discontinuation. 91% is not "close enough" — it is a documented performance gap.',f:'❌ 95% is the standard, not a target. Below it triggers a formal conversation. Two occurrences within 60 days escalates to reassignment or discontinuation. There is no acceptable margin of error.'},
  'q17': {t:'✅ At minimum 5 missing providers: ambulance/EMS, ER physician group (separate from Grady), Grady radiology group, Peachtree Imaging, Dr. Patel orthopedic, and ATL Rehab PT. Each bills separately.',f:'❌ Hospital facility records do not include the ER physician, radiology, or ambulance. Each is a separate entity. Plus Peachtree Imaging, Dr. Patel, and ATL Rehab. That is at least 5-6 missing requests.'},
  'q18': {t:'✅ Flag immediately. The demand CANNOT go out with 5+ missing providers — every missing bill is damages left off the table. The paralegal needs to know before the demand ships.',f:'❌ Do not send requests first and notify later, do not let the demand go out incomplete, and do not question whether the records are needed. Flag the gap to the paralegal immediately with the specific list.'},
  'q19': {t:'✅ All requests go out the same day. Every day of delay extends the demand hold. Simultaneous requests, 14-day follow-ups set for each, everything logged in CasePeer immediately.',f:'❌ Never stagger records requests when a demand is waiting. All providers get requests the same day. Set individual 14-day follow-up tasks for each. Log everything immediately. Speed is the priority.'},
  'q20': {t:'✅ Third and final attempt: call at a different time, get a specific person\'s name in billing, document the full conversation. If this fails, the next step is paralegal escalation for attorney intervention.',f:'❌ The third attempt should maximize chances of success: different time of day, specific person in billing, full documentation. Faxing again, escalating early, or visiting in person are not the standard procedure.'}
}"""
src = src[:fb_start] + new_fb + src[fb_end:]

# ── 9. FIX CONSTANTS ──
src = src.replace('var PASS_THRESHOLD = 170;', 'var PASS_THRESHOLD = 160;')

# ── 10. CERTIFICATE TEXT ──
src = src.replace('Day 10: Week 2 Review &amp; Assessment', 'LA-1: Records Retrieval &amp; Follow-Up')
src = src.replace("'Day 10: Week 2 Review &amp; Assessment'", "'LA-1: Records Retrieval &amp; Follow-Up'")
src = src.replace("'🎓 Day 10 Complete'", "'🎓 LA-1 Complete'")
src = src.replace("'60-Day Gate Cleared'", "'LA Track Started'")
src = src.replace('role-specific training tracks where you apply these skills in your exact position.', 'the next LA module. Every skill tested here is now part of your daily workflow.')

# ── 11. SECTION SCORE LABELS ──
src = src.replace(
    "sectionIdx <= 5 ? (pts + ' / 40') : (pts + ' bonus pts earned')",
    "sectionIdx <= 3 ? (pts + ' / 30') : sectionIdx <= 5 ? (pts + ' / 40') : (pts + ' bonus pts earned')"
)

# ── 12. WRITE ──
with open('site/module-la1.html', 'w') as f:
    f.write(src)

print(f"Written: site/module-la1.html ({len(src)} bytes)")

# Verify
import subprocess
def gc(pat):
    r = subprocess.run(['grep', '-ci', pat, 'site/module-la1.html'], capture_output=True, text=True)
    return r.stdout.strip() or '0'
def ge(pat):
    r = subprocess.run(['grep', '-c', pat, 'site/module-la1.html'], capture_output=True, text=True)
    return r.stdout.strip() or '0'

print(f"label the emotion: {gc('label the emotion')}")
print(f"voss/mirroring/ackerman: {gc('voss')}, {gc('mirroring')}, {gc('ackerman')}")
print(f"GLG-2026-0731: {ge('GLG-2026-0731')}")
print(f"glg-logo: {ge('glg-logo')}")
print(f"gavelMascot: {ge('gavelMascot')}")
print(f"Math.min: {ge('Math.min')}")
print(f"TRACKER_URL: {ge('TRACKER_URL')}")

r = subprocess.run(['grep', '-o', "correct:'[a-d]'", 'site/module-la1.html'], capture_output=True, text=True)
from collections import Counter
letters = [l.split("'")[1] for l in r.stdout.strip().split('\n') if l]
c = Counter(letters)
print(f"Answer distribution: {dict(c)}")

# Distractor parity check
import re
with open('site/module-la1.html') as f: html = f.read()
opts = re.findall(r'onclick="answer\(\'(q\d+)\',\'([a-d])\',(?:true|false)\)"[^>]*><span class="opt-letter">[A-D]</span><span class="opt-text">(.*?)</span>', html)
from collections import defaultdict
qs = defaultdict(dict)
for qid, letter, text in opts:
    qs[qid][letter] = len(text.split())
print("\nDistractor Parity:")
for qid in sorted(qs.keys(), key=lambda x: int(x[1:])):
    v = qs[qid]
    a,b,c,d = v.get('a',0),v.get('b',0),v.get('c',0),v.get('d',0)
    mx,mn = max(a,b,c,d), min(x for x in [a,b,c,d] if x>0)
    pct = round((mx-mn)/mx*100)
    flag = '🔴' if pct>30 else '🟡' if pct>20 else '✅'
    print(f"  {qid}: A={a} B={b} C={c} D={d} | {pct}% {flag}")
