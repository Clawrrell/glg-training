#!/usr/bin/env python3
"""Build LA-1 from NH-11 polished chassis."""
import re, subprocess
from collections import Counter, defaultdict

with open('site/module-nh11.html', 'r') as f:
    src = f.read()

# ── SIMPLE STRING SWAPS ──
swaps = [
    ('NH-11', 'LA-1'),
    ('Week 2 Review', 'Records Retrieval'),
    ("'nh11'", "'la1'"),
    ('"nh11"', '"la1"'),
    ('NH-11 Week 2 Review & Assessment', 'LA-1 Records Retrieval & Follow-Up'),
    ('Week 2 Review &amp; Assessment', 'Records Retrieval &amp; Follow-Up'),
    ('Week 2 Capstone', 'LA Track Day 1'),
    ('Days 6–10', 'Pre-Lit Records'),
    ('all banned terms verified zero', 'all banned terms verified zero'),
    ('Teresa Ramirez', 'Marcus Thompson'),
    ('GLG-2026-1192', 'GLG-2026-0731'),
    ('Week 2 Gate Cleared', 'LA Track Started'),
    ('the next phase of training.', 'the next LA module.'),
    ('NH-11 Complete', 'LA-1 Complete'),
    ('Gunn Law Group · Legal Assistant Training', 'Gunn Law Group · Legal Assistant Track'),
]
for old, new in swaps:
    src = src.replace(old, new)

# ── NAV PILLS ──
src = src.replace(
    ">1. Intro<", ">1. Intro<"
).replace(
    ">2. Records<", ">2. Your Role<"
).replace(
    ">3. Coverage<", ">3. Requests<"
).replace(
    ">4. Liens<", ">4. Providers<"
).replace(
    ">5. Comms<", ">5. Follow-Up<"
).replace(
    ">6. Treatment<", ">6. CasePeer<"
)

# ── REPLACE SECTIONS 0-6 ──
# The section HTML and Q_CONFIG/FEEDBACK from the NH-11 build script were already
# adapted for this chassis. We just need to swap content.
# Read the LA-1 specific content from build-la1.py
exec(open('build-la1.py').read().split("# ── 5. REPLACE SECTIONS")[1].split("# ── 6. Q_CONFIG")[0])

# This approach is getting complex. Let me just do targeted replacements on the
# question text, feedback, and section headers.

# Actually, the simplest approach: the NH-11 chassis already has the right
# infrastructure (Q_CONFIG, FEEDBACK, answer(), gamification). I just need to
# replace the CONTENT of each question and section.

print("Note: Using dedicated section injection approach instead")
