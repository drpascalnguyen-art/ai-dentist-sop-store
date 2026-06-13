"""
Generate FULL paid deliverable PDFs for Gumroad SOP Store.
Run from: /Users/pascalnguyen/Documents/New project/lemon-squeezy-store/sample-docs/
"""

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

BRAND_COLOR = colors.HexColor("#1a1a2e")
ACCENT_COLOR = colors.HexColor("#4361ee")
LIGHT_GRAY = colors.HexColor("#f8f8f8")
MID_GRAY = colors.HexColor("#666666")

FOOTER = "© 2026 Dr. Pascal Nguyen, DMD, NMD / PJN Dental — Educational and business workflow resource. Not clinical, legal, financial, or HIPAA compliance advice."


def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("title", parent=base["Title"],
            fontSize=22, textColor=BRAND_COLOR, spaceAfter=6, leading=26),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"],
            fontSize=11, textColor=MID_GRAY, spaceAfter=20, leading=14),
        "h2": ParagraphStyle("h2", parent=base["Heading2"],
            fontSize=13, textColor=BRAND_COLOR, spaceBefore=16, spaceAfter=6, leading=16),
        "h3": ParagraphStyle("h3", parent=base["Heading3"],
            fontSize=11, textColor=ACCENT_COLOR, spaceBefore=10, spaceAfter=4, leading=14),
        "body": ParagraphStyle("body", parent=base["Normal"],
            fontSize=10, textColor=colors.black, leading=14, spaceAfter=6),
        "bullet": ParagraphStyle("bullet", parent=base["Normal"],
            fontSize=10, textColor=colors.black, leading=14, spaceAfter=4,
            leftIndent=16, bulletIndent=4),
        "footer": ParagraphStyle("footer", parent=base["Normal"],
            fontSize=8, textColor=MID_GRAY, leading=10, alignment=TA_CENTER),
        "notice": ParagraphStyle("notice", parent=base["Normal"],
            fontSize=9, textColor=MID_GRAY, leading=12, spaceAfter=6,
            leftIndent=12, rightIndent=12),
        "label": ParagraphStyle("label", parent=base["Normal"],
            fontSize=9, textColor=ACCENT_COLOR, leading=12, spaceAfter=2),
    }
    return styles


def build_pdf(filename, title, subtitle, sections, footer_line):
    doc = SimpleDocTemplate(
        filename,
        pagesize=LETTER,
        rightMargin=1*inch,
        leftMargin=1*inch,
        topMargin=1*inch,
        bottomMargin=1*inch,
    )
    s = make_styles()
    story = []
    story.append(Paragraph(title, s["title"]))
    story.append(Paragraph(subtitle, s["subtitle"]))
    story.append(Spacer(1, 6))

    for section in sections:
        t = section["type"]
        if t == "heading":
            story.append(Paragraph(section["text"], s["h2"]))
        elif t == "subheading":
            story.append(Paragraph(section["text"], s["h3"]))
        elif t == "body":
            story.append(Paragraph(section["text"], s["body"]))
        elif t == "bullet":
            for item in section["items"]:
                story.append(Paragraph(f"• {item}", s["bullet"]))
            story.append(Spacer(1, 4))
        elif t == "numbered":
            for i, item in enumerate(section["items"], 1):
                story.append(Paragraph(f"{i}. {item}", s["bullet"]))
            story.append(Spacer(1, 4))
        elif t == "table":
            tdata = [section["headers"]] + section["rows"]
            col_widths = section.get("colWidths")
            tbl = Table(tdata, hAlign="LEFT", colWidths=col_widths)
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), ACCENT_COLOR),
                ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                ("FONTSIZE", (0,0), (-1,0), 9),
                ("FONTSIZE", (0,1), (-1,-1), 9),
                ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
                ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
                ("LEFTPADDING", (0,0), (-1,-1), 6),
                ("RIGHTPADDING", (0,0), (-1,-1), 6),
                ("TOPPADDING", (0,0), (-1,-1), 4),
                ("BOTTOMPADDING", (0,0), (-1,-1), 4),
                ("VALIGN", (0,0), (-1,-1), "TOP"),
            ]))
            story.append(tbl)
            story.append(Spacer(1, 8))
        elif t == "notice":
            story.append(Paragraph(section["text"], s["notice"]))
        elif t == "label":
            story.append(Paragraph(section["text"], s["label"]))
        elif t == "space":
            story.append(Spacer(1, section.get("size", 8)))
        elif t == "pagebreak":
            story.append(PageBreak())

    story.append(Spacer(1, 24))
    story.append(Paragraph(footer_line, s["footer"]))
    doc.build(story)
    print(f"Generated: {filename}")


# ─── PRODUCT 1: AI Dentist SOP Starter Pack ($49) ────────────────────────────

build_pdf(
    "ai-dentist-sop-starter-pack-FULL.pdf",
    "AI Dentist SOP Starter Pack",
    "Starter SOPs, workflow templates, and checklists for dental teams adopting AI tools — by Dr. Pascal Nguyen, DMD, NMD / PJN Dental",
    [
        {"type": "notice", "text":
         "These templates are educational and business workflow resources. They are not legal, financial, medical, clinical, regulatory, or HIPAA compliance advice. "
         "Adapt all templates to your jurisdiction, practice policies, and professional standards."},
        {"type": "space", "size": 8},

        # Section 1: AI Use-Case Inventory Worksheet
        {"type": "heading", "text": "1. AI Use-Case Inventory Worksheet"},
        {"type": "body", "text":
         "Use this worksheet once per quarter to map every AI tool your team is using or considering. "
         "The goal is one clear list of approved use cases, responsible owners, and any outstanding review gaps."},
        {"type": "subheading", "text": "How To Complete"},
        {"type": "numbered", "items": [
            "List every AI tool currently in use (include free tools and browser extensions).",
            "For each tool, identify the task category: admin, marketing, scheduling, documentation support, or other.",
            "Mark whether each use involves protected health information (PHI). Any PHI use requires a separate HIPAA review — consult your compliance officer.",
            "Assign one owner per tool — the team member accountable for appropriate use.",
            "Flag gaps: tools with no owner, no use-case boundary, or no review process.",
        ]},
        {"type": "subheading", "text": "Inventory Table"},
        {"type": "table",
         "headers": ["AI Tool", "Task Category", "PHI Involved?", "Owner", "Approved Use Cases", "Review Gap"],
         "colWidths": [80, 80, 65, 75, 130, 60],
         "rows": [
             ["Example: ChatGPT", "Marketing drafts", "No", "Front desk lead", "First-draft patient education posts, reviewed before publish", "None"],
             ["Example: Whisper", "Meeting notes", "No", "Office manager", "Transcribing non-patient team meetings", "None"],
             ["[Add your tool]", "", "", "", "", ""],
             ["[Add your tool]", "", "", "", "", ""],
             ["[Add your tool]", "", "", "", "", ""],
         ]},
        {"type": "body", "text":
         "Review this table with your team lead at least once per quarter. Remove any tool that cannot be assigned a clear owner and approved use case."},

        # Section 2: Team Workflow SOP Templates
        {"type": "pagebreak"},
        {"type": "heading", "text": "2. Team Workflow SOP Templates"},
        {"type": "body", "text":
         "Use these three templates as starting points. Copy, adapt, and save in your practice's internal documentation system."},

        {"type": "subheading", "text": "SOP Template A — AI-Assisted Content Draft Review"},
        {"type": "label", "text": "PURPOSE"},
        {"type": "body", "text":
         "Ensure all AI-drafted content passes a human review before use in any patient-facing, public, or internal channel."},
        {"type": "label", "text": "TRIGGER"},
        {"type": "body", "text":
         "Any time an AI tool produces text, images, or summaries intended for use by the practice."},
        {"type": "label", "text": "STEPS"},
        {"type": "numbered", "items": [
            "Request the draft using an approved prompt from the Prompt Safety and Review Checklist (Section 3).",
            "Read the output in full before using or sharing.",
            "Check against the Human Review Standard below.",
            "Edit or reject any content that fails a check.",
            "Save the approved final version in the designated folder.",
            "Log the task: tool used, task category, reviewer initials, date.",
        ]},
        {"type": "label", "text": "HUMAN REVIEW STANDARD"},
        {"type": "bullet", "items": [
            "No diagnosis, clinical recommendation, or treatment instruction.",
            "No guarantee of outcome, cure, or reversal.",
            "No representation as professional, legal, or compliance advice.",
            "No patient-identifying information in any AI input.",
            "Tone is clear, warm, and non-alarming.",
            "Any factual claim has a source the reviewer can verify.",
        ]},
        {"type": "label", "text": "OWNER"},
        {"type": "body", "text": "Designated team member (assign one name, not a role category)."},

        {"type": "space", "size": 12},
        {"type": "subheading", "text": "SOP Template B — New AI Tool Adoption"},
        {"type": "label", "text": "PURPOSE"},
        {"type": "body", "text":
         "Create a consistent approval gate before any new AI tool is used by the team, even for a trial."},
        {"type": "label", "text": "STEPS"},
        {"type": "numbered", "items": [
            "Identify the tool and the specific task it will support.",
            "Check: does this tool require patient data? If yes, STOP — escalate to your compliance officer.",
            "Identify a limited trial scope: one person, one task, two weeks.",
            "Add the tool to the AI Use-Case Inventory Worksheet.",
            "Assign an owner and define approved use cases before the trial starts.",
            "Review after two weeks: approve, modify scope, or remove.",
        ]},

        {"type": "space", "size": 12},
        {"type": "subheading", "text": "SOP Template C — AI Output Escalation"},
        {"type": "label", "text": "PURPOSE"},
        {"type": "body", "text":
         "Define what to do when AI output is unclear, potentially inaccurate, or touches a sensitive area."},
        {"type": "label", "text": "ESCALATION TRIGGERS"},
        {"type": "bullet", "items": [
            "Output includes clinical-sounding language (symptoms, diagnoses, medications).",
            "Output references a specific patient, even if only by context.",
            "Output makes a regulatory or compliance claim.",
            "Reviewer is unsure whether the output is accurate.",
        ]},
        {"type": "label", "text": "STEPS"},
        {"type": "numbered", "items": [
            "Do not use or share the output.",
            "Flag the output for the tool owner.",
            "The owner reviews and either clears, edits, or discards.",
            "If the output involves PHI or a clinical claim, escalate to the practice lead immediately.",
            "Log the escalation: date, tool, task, resolution.",
        ]},

        # Section 3: Prompt Safety and Review Checklist
        {"type": "pagebreak"},
        {"type": "heading", "text": "3. Prompt Safety and Review Checklist"},
        {"type": "body", "text":
         "Use this checklist every time you write a prompt for an AI tool. A safe prompt produces safer output and reduces review time downstream."},

        {"type": "subheading", "text": "Before You Write The Prompt"},
        {"type": "bullet", "items": [
            "Confirm the task does not require entering any patient-identifying information.",
            "Confirm the task falls within an approved use category (see Inventory Worksheet).",
            "Confirm you are using an approved tool.",
        ]},

        {"type": "subheading", "text": "Prompt Construction Checklist"},
        {"type": "table",
         "headers": ["Prompt Element", "Guideline", "Why It Matters"],
         "colWidths": [100, 200, 160],
         "rows": [
             ["Task description", "State what you need clearly and specifically.", "Vague prompts produce unpredictable output."],
             ["Audience", "Name the intended reader (e.g., 'a dental patient with no clinical background').", "AI adjusts tone and complexity to the audience you specify."],
             ["Tone boundary", "State if you want warm, professional, or educational — not alarmist.", "Helps avoid output that could cause patient anxiety."],
             ["Content boundary", "Include: 'Do not include diagnosis, clinical advice, or guaranteed outcomes.'", "Reduces the chance of unsafe clinical-sounding language."],
             ["Review instruction", "End with: 'This is a first draft for human review.'", "Signals that the output is a starting point, not a final product."],
         ]},

        {"type": "subheading", "text": "After You Receive The Output"},
        {"type": "numbered", "items": [
            "Read the full output before using any part of it.",
            "Run the Human Review Standard from SOP Template A.",
            "Edit or reject anything that fails.",
            "Save approved output with the log entry (tool, task, reviewer, date).",
        ]},

        {"type": "subheading", "text": "Prompt Templates You Can Copy"},
        {"type": "label", "text": "ADMIN TASK PROMPT"},
        {"type": "body", "text":
         "Create a [type of document — e.g., checklist / SOP outline / meeting agenda] for a dental practice team. "
         "The audience is non-clinical admin staff. Keep the tone professional and clear. "
         "Do not include clinical, medical, legal, or HIPAA compliance advice. "
         "This is a first draft for human review and editing."},
        {"type": "space", "size": 8},
        {"type": "label", "text": "EDUCATIONAL CONTENT PROMPT"},
        {"type": "body", "text":
         "Write a patient-friendly educational post about [TOPIC] for a dental practice. "
         "Tone: warm, clear, non-alarming. "
         "Do not include diagnosis, treatment recommendations, or guaranteed outcomes. "
         "Use language like 'may,' 'can,' or 'is associated with' where appropriate. "
         "Include a reminder to discuss individual concerns with a dental or medical professional. "
         "This is a first draft for human review before publishing."},

        {"type": "space", "size": 16},
        {"type": "subheading", "text": "Quick Reference — Approved vs. Not Approved"},
        {"type": "table",
         "headers": ["Approved", "Not Approved Without Additional Review"],
         "colWidths": [240, 270],
         "rows": [
             ["Drafting internal admin checklists", "Entering patient names or health data into any AI tool"],
             ["Creating first-draft educational content", "Generating diagnosis, treatment, or medication instructions"],
             ["Summarizing non-patient team meetings", "Publishing any AI output without human review"],
             ["Organizing recurring admin workflows", "Representing AI output as professional or legal advice"],
             ["Drafting practice policy outlines", "Using unapproved tools on any patient-facing task"],
         ]},
    ],
    FOOTER
)


# ─── PRODUCT 2: AI Dental Marketing Prompt Pack ($79) ────────────────────────

build_pdf(
    "ai-dental-marketing-prompt-pack-FULL.pdf",
    "AI Dental Marketing Prompt Pack",
    "Prompt library, content review workflows, and campaign planning worksheets for dental teams — by Dr. Pascal Nguyen, DMD, NMD / PJN Dental",
    [
        {"type": "notice", "text":
         "These templates are educational and business workflow resources. They are not legal, financial, medical, clinical, regulatory, or HIPAA compliance advice. "
         "Adapt all templates to your jurisdiction, practice policies, professional standards, and applicable advertising regulations."},
        {"type": "space", "size": 8},

        # Section 1: Prompt Library
        {"type": "heading", "text": "1. Prompt Library — Patient-Friendly Education"},
        {"type": "body", "text":
         "Each prompt below is a tested starting point. Copy and customize for your practice voice. "
         "Every output must pass the Content Review Checklist in Section 2 before publishing."},

        {"type": "subheading", "text": "How To Use These Prompts"},
        {"type": "numbered", "items": [
            "Replace [bracketed placeholders] with your specific topic or context.",
            "Paste the prompt into your approved AI tool.",
            "Read the full output before using any part.",
            "Run the Content Review Checklist (Section 2).",
            "Edit, then publish or file.",
        ]},

        {"type": "subheading", "text": "Prompt 1 — General Educational Post"},
        {"type": "body", "text":
         "Write a patient-friendly educational post about [TOPIC] for a dental practice social media channel or newsletter. "
         "Audience: general adult patients with no clinical background. "
         "Tone: warm, clear, non-alarming. Length: 150–200 words. "
         "Do not include diagnosis, clinical recommendations, guaranteed outcomes, or before-and-after claims. "
         "Use 'may,' 'can,' or 'is associated with' where appropriate. "
         "End with a gentle prompt to schedule a consultation or ask a question at their next visit. "
         "This is a first draft for human review."},

        {"type": "subheading", "text": "Prompt 2 — Biological / Holistic Dentistry Education"},
        {"type": "body", "text":
         "Write an educational post explaining [TOPIC — e.g., the connection between oral health and systemic wellness / what biological dentistry considers / why materials matter] "
         "for a biological dental practice audience. "
         "Tone: curious, evidence-respectful, non-alarming. Length: 150–250 words. "
         "Do not make cure, reversal, or treatment promises. Avoid language that positions biological dentistry against conventional dentistry. "
         "Frame as 'a perspective worth discussing with your dental team.' "
         "This is a first draft for human review."},

        {"type": "subheading", "text": "Prompt 3 — FAQ Response Draft"},
        {"type": "body", "text":
         "Draft a warm, clear answer to this common patient question: '[PASTE QUESTION].' "
         "Audience: general dental patients. Tone: reassuring, plain language. "
         "Do not diagnose, prescribe, or guarantee outcomes. "
         "If the answer depends on individual factors, note that patients should discuss their specific situation at a consultation. "
         "Length: 100–150 words. This is a first draft for human review."},

        {"type": "subheading", "text": "Prompt 4 — Newsletter Section Draft"},
        {"type": "body", "text":
         "Write a newsletter section on [TOPIC] for a biological dental practice. "
         "Tone: warm, educational, conversational. Length: 200–300 words. "
         "Include: a brief explanation of why this topic matters to patients, one practical takeaway, and a soft call to action (schedule, ask a question, reply to this email). "
         "Do not include clinical advice, diagnosis, or guaranteed outcomes. "
         "This is a first draft for human review."},

        {"type": "subheading", "text": "Prompt 5 — Social Caption (Short)"},
        {"type": "body", "text":
         "Write a 1–3 sentence social media caption about [TOPIC] for a dental practice. "
         "Tone: warm and approachable. Do not include clinical claims, guarantees, or before-and-after promises. "
         "End with a simple question or invitation to learn more. "
         "This is a first draft for human review."},

        {"type": "subheading", "text": "Prompt 6 — Team Training Content"},
        {"type": "body", "text":
         "Write a brief internal training note for a dental team explaining [TOPIC — e.g., how to answer patient questions about AI tools / how to respond to questions about holistic dentistry / our position on mercury-free dentistry]. "
         "Audience: front desk and clinical support staff. Tone: professional, straightforward. "
         "Length: 200–250 words. "
         "This is a first draft for team lead review."},

        {"type": "subheading", "text": "Prompt 7 — Objection Response Draft"},
        {"type": "body", "text":
         "Draft a warm response to this patient concern: '[PASTE OBJECTION OR CONCERN].' "
         "Tone: empathetic, clear, non-defensive. "
         "Acknowledge the concern, provide one or two clear, factual points, and invite the patient to discuss further at a consultation. "
         "Do not promise outcomes or dismiss the concern. "
         "Length: 100–150 words. This is a first draft for human review."},

        {"type": "subheading", "text": "Prompt 8 — Referral or Partnership Outreach Draft"},
        {"type": "body", "text":
         "Draft a professional outreach message to [TYPE OF PROVIDER — e.g., a naturopathic doctor / a myofunctional therapist / a sleep medicine physician] "
         "introducing our biological dental practice and exploring a referral or collaboration relationship. "
         "Tone: collegial, respectful, specific about what we do. Length: 150–200 words. "
         "Do not make clinical claims. This is a first draft for review before sending."},

        # Section 2: Content Review Checklist
        {"type": "pagebreak"},
        {"type": "heading", "text": "2. Content Review and Claims Checklist"},
        {"type": "body", "text":
         "Run every AI-generated piece of content through this checklist before using or publishing it. "
         "One 'No' answer stops publication until the issue is resolved."},

        {"type": "subheading", "text": "Pass / Fail Checklist"},
        {"type": "table",
         "headers": ["Check", "Pass If...", "Fail If..."],
         "colWidths": [100, 195, 195],
         "rows": [
             ["No diagnosis", "Content describes general topics or possibilities.", "Content names or implies a diagnosis for a reader."],
             ["No treatment instruction", "Content discusses what practices consider, not what a patient should do.", "Content tells readers to take a specific clinical action."],
             ["No outcome guarantee", "Language uses 'may,' 'can,' 'is associated with.'", "Language says 'will,' 'cures,' 'reverses,' 'eliminates.'"],
             ["No before-and-after promise", "Visual or text results are absent or clearly sourced.", "Content implies predictable individual results."],
             ["No patient-specific advice", "Content is general and educational.", "Content responds to a named or implied individual's health situation."],
             ["No unsupported claim", "Any factual claim has a source the reviewer can verify.", "A claim cannot be sourced or is outside reviewer expertise."],
             ["Regulatory language present", "'Results may vary' or equivalent where appropriate.", "Guaranteed, absolute, or superlative outcome language used."],
             ["Disclaimer present", "Post includes or links to the practice's content disclaimer.", "No disclaimer, especially on sensitive health topics."],
             ["Tone passes", "Warm, clear, non-alarming, not dismissive of conventional care.", "Alarmist, fear-based, or positions practice against competitors."],
             ["Human reviewed", "A team member read it in full and signed off.", "Published directly from AI output without review."],
         ]},

        {"type": "subheading", "text": "Content Disclaimer (Use As-Is or Adapt)"},
        {"type": "notice", "text":
         "This content is for educational purposes only. It is not a substitute for professional dental or medical advice, diagnosis, or treatment. "
         "Always consult a qualified dental or medical professional for questions about your specific health situation."},

        # Section 3: Monthly Campaign Planning Worksheet
        {"type": "pagebreak"},
        {"type": "heading", "text": "3. Monthly Campaign Planning Worksheet"},
        {"type": "body", "text":
         "Use this worksheet at the start of each month to plan content before you produce it. "
         "Planned content is more consistent, less reactive, and easier to review."},

        {"type": "subheading", "text": "Month Overview"},
        {"type": "table",
         "headers": ["Field", "Your Entry"],
         "colWidths": [150, 350],
         "rows": [
             ["Month / Year", ""],
             ["Primary topic theme this month", ""],
             ["Secondary topic (if any)", ""],
             ["Key practice milestone or event", ""],
             ["Content owner (who is producing?)", ""],
             ["Review owner (who approves?)", ""],
             ["Publishing channels", ""],
         ]},

        {"type": "subheading", "text": "Weekly Content Plan"},
        {"type": "table",
         "headers": ["Week", "Channel", "Topic", "Format", "Prompt Used", "Review Owner", "Status"],
         "colWidths": [35, 65, 100, 55, 80, 75, 50],
         "rows": [
             ["Wk 1", "", "", "", "", "", "Draft"],
             ["Wk 1", "", "", "", "", "", "Draft"],
             ["Wk 2", "", "", "", "", "", "Draft"],
             ["Wk 2", "", "", "", "", "", "Draft"],
             ["Wk 3", "", "", "", "", "", "Draft"],
             ["Wk 3", "", "", "", "", "", "Draft"],
             ["Wk 4", "", "", "", "", "", "Draft"],
             ["Wk 4", "", "", "", "", "", "Draft"],
         ]},

        {"type": "subheading", "text": "Format Definitions"},
        {"type": "table",
         "headers": ["Format", "Definition", "Typical Length"],
         "colWidths": [90, 270, 130],
         "rows": [
             ["Educational post", "Patient-facing content explaining a dental health topic.", "150–250 words"],
             ["FAQ response", "Answer to a common patient question.", "100–150 words"],
             ["Newsletter section", "One section of a practice email newsletter.", "200–300 words"],
             ["Social caption", "Short social media text, image optional.", "1–3 sentences"],
             ["Team note", "Internal communication for staff.", "200–250 words"],
         ]},

        {"type": "subheading", "text": "Monthly Review"},
        {"type": "numbered", "items": [
            "Count posts planned vs. published.",
            "Note which topics got the most engagement or questions.",
            "Identify any review bottlenecks (too long in review, rejected drafts).",
            "Update the Prompt Library with any new prompts that worked well.",
            "Set next month's primary topic theme.",
        ]},
    ],
    FOOTER
)


# ─── PRODUCT 3: Clinical Admin Workflow SOP Bundle ($149) ─────────────────────

build_pdf(
    "clinical-admin-workflow-sop-bundle-FULL.pdf",
    "Clinical Admin Workflow SOP Bundle",
    "Admin handoff templates, meeting and task-routing SOPs, and quality-control checklists for dental teams — by Dr. Pascal Nguyen, DMD, NMD / PJN Dental",
    [
        {"type": "notice", "text":
         "These templates are educational and business workflow resources. They are not legal, financial, medical, clinical, regulatory, or HIPAA compliance advice. "
         "Adapt all templates to your jurisdiction, practice policies, compliance requirements, and professional standards."},
        {"type": "space", "size": 8},

        # Section 1: Admin Handoff Templates
        {"type": "heading", "text": "1. Admin Handoff Templates"},
        {"type": "body", "text":
         "Handoff failures are one of the most common sources of dropped tasks in dental practices. "
         "Use these templates to create clean handoffs at shift changes, during provider transitions, and across team roles."},

        {"type": "subheading", "text": "Handoff Template A — Daily End-of-Day Admin Handoff"},
        {"type": "label", "text": "PURPOSE"},
        {"type": "body", "text":
         "Ensure the closing team member passes all open administrative items to the next shift or next-day opener with zero gaps."},
        {"type": "label", "text": "FIELDS"},
        {"type": "table",
         "headers": ["Field", "Entry"],
         "colWidths": [180, 330],
         "rows": [
             ["Date", ""],
             ["Closing team member", ""],
             ["Opening team member (next day)", ""],
             ["Outstanding insurance or billing items", ""],
             ["Calls not returned today", ""],
             ["Appointments needing confirmation tomorrow", ""],
             ["Supply or vendor follow-ups open", ""],
             ["Any patient access or record requests pending", ""],
             ["Open front-desk tasks requiring action", ""],
             ["Doctor / provider requests outstanding", ""],
             ["Notes for opener", ""],
         ]},
        {"type": "label", "text": "DELIVERY"},
        {"type": "body", "text":
         "This form is completed before end of day and left in the opener's physical inbox or sent via internal secure message. "
         "Do not include patient PHI in any unsecured channel."},

        {"type": "space", "size": 10},
        {"type": "subheading", "text": "Handoff Template B — Provider Transition Handoff"},
        {"type": "label", "text": "PURPOSE"},
        {"type": "body", "text":
         "Used when a provider leaves for the day mid-schedule or transfers a patient's administrative workflow to another team member."},
        {"type": "label", "text": "FIELDS"},
        {"type": "table",
         "headers": ["Field", "Entry"],
         "colWidths": [180, 330],
         "rows": [
             ["Date / Time", ""],
             ["Handing off from", ""],
             ["Handing off to", ""],
             ["Outstanding administrative items", ""],
             ["Referral or lab follow-ups open", ""],
             ["Scheduling tasks remaining", ""],
             ["Patient communications outstanding (no PHI in this form)", ""],
             ["Special notes", ""],
         ]},

        {"type": "space", "size": 10},
        {"type": "subheading", "text": "Handoff Template C — Role Transition Handoff (New Hire / Coverage)"},
        {"type": "label", "text": "PURPOSE"},
        {"type": "body", "text":
         "Used when a team member covers another role temporarily or a new hire takes over a function."},
        {"type": "numbered", "items": [
            "List every recurring task in the role (daily, weekly, monthly).",
            "Assign a 'buddy' who can answer questions for the first week.",
            "Walk through the task list once before the transition.",
            "Schedule a 3-day check-in to address gaps.",
            "Complete the handoff template and file it in the role's documentation folder.",
        ]},

        # Section 2: Meeting and Task-Routing SOPs
        {"type": "pagebreak"},
        {"type": "heading", "text": "2. Meeting and Task-Routing SOPs"},

        {"type": "subheading", "text": "SOP 2A — Weekly Team Huddle"},
        {"type": "label", "text": "CADENCE"},
        {"type": "body", "text": "Weekly, Monday morning. Duration: 15 minutes maximum."},
        {"type": "label", "text": "AGENDA FORMAT"},
        {"type": "table",
         "headers": ["Time", "Agenda Item", "Owner"],
         "colWidths": [60, 300, 130],
         "rows": [
             ["0:00–2:00", "Open loop review: what was left open from last week?", "Meeting lead"],
             ["2:00–7:00", "This week's priorities: top 3 admin or operational items.", "Each department"],
             ["7:00–12:00", "Task assignments: who owns what this week?", "Meeting lead"],
             ["12:00–14:00", "Blockers: what is stopping anyone from completing their tasks?", "All"],
             ["14:00–15:00", "Close: confirm next meeting time.", "Meeting lead"],
         ]},
        {"type": "label", "text": "OUTPUT"},
        {"type": "body", "text":
         "One page of action items with owners and due dates, filed in the team's shared folder. "
         "Use the Meeting Notes to Action Register template below."},

        {"type": "space", "size": 10},
        {"type": "subheading", "text": "SOP 2B — Meeting Notes to Action Register"},
        {"type": "body", "text":
         "After every team meeting, convert raw notes into this action register format within 24 hours."},
        {"type": "table",
         "headers": ["Action Item", "Owner", "Due Date", "Dependency", "Status"],
         "colWidths": [150, 80, 65, 110, 60],
         "rows": [
             ["[Describe the specific task]", "[Name]", "[Date]", "[What must happen first, or 'None']", "Open"],
             ["", "", "", "", ""],
             ["", "", "", "", ""],
             ["", "", "", "", ""],
             ["", "", "", "", ""],
         ]},
        {"type": "label", "text": "STATUS DEFINITIONS"},
        {"type": "bullet", "items": [
            "Open — not started or in progress.",
            "Blocked — waiting on another action or person.",
            "Done — completed and documented.",
            "Parked — deferred intentionally with a review date.",
        ]},

        {"type": "space", "size": 10},
        {"type": "subheading", "text": "SOP 2C — Task Routing Protocol"},
        {"type": "label", "text": "PURPOSE"},
        {"type": "body", "text":
         "Every incoming task must be routed to a single owner within 24 hours. Tasks without an owner disappear."},
        {"type": "label", "text": "ROUTING RULES"},
        {"type": "table",
         "headers": ["Task Type", "Default Owner", "Escalate To If Unresolved"],
         "colWidths": [150, 150, 200],
         "rows": [
             ["Scheduling, recalls, confirmations", "Front desk lead", "Office manager"],
             ["Insurance, billing, claims", "Billing coordinator", "Office manager"],
             ["Lab, supply, vendor orders", "Assigned admin", "Office manager"],
             ["Referral coordination", "Patient coordinator", "Provider or office manager"],
             ["Team communication issues", "Office manager", "Practice lead / doctor"],
             ["Technology or software issues", "Designated tech owner", "Office manager or vendor"],
             ["Unrouted / unclear tasks", "Office manager", "Practice lead"],
         ]},
        {"type": "label", "text": "ESCALATION RULE"},
        {"type": "body", "text":
         "Any task not resolved or routed within 48 hours is escalated to the office manager. "
         "Tasks not resolved within 5 business days go to the practice lead."},

        # Section 3: Quality-Control Checklists
        {"type": "pagebreak"},
        {"type": "heading", "text": "3. Quality-Control Checklists"},

        {"type": "subheading", "text": "QC Checklist A — Weekly Admin Quality Check"},
        {"type": "body", "text":
         "Complete every Friday before close. The office manager or designated lead signs off."},
        {"type": "table",
         "headers": ["Item", "Check", "Notes"],
         "colWidths": [220, 80, 200],
         "rows": [
             ["All open action items from Monday huddle closed or updated.", "Yes / No", ""],
             ["No unanswered patient calls older than 24 hours.", "Yes / No", ""],
             ["All appointment confirmations for next week sent.", "Yes / No", ""],
             ["Insurance and billing follow-ups addressed this week.", "Yes / No", ""],
             ["Supply and vendor orders placed or confirmed.", "Yes / No", ""],
             ["Referral follow-ups completed or flagged.", "Yes / No", ""],
             ["End-of-day handoff forms completed.", "Yes / No", ""],
             ["Team member issues or conflicts flagged to manager.", "Yes / No", ""],
             ["Next week's priority list drafted.", "Yes / No", ""],
         ]},
        {"type": "label", "text": "SIGN-OFF"},
        {"type": "table",
         "headers": ["Reviewer", "Date", "Notes"],
         "colWidths": [170, 100, 230],
         "rows": [
             ["", "", ""],
         ]},

        {"type": "space", "size": 10},
        {"type": "subheading", "text": "QC Checklist B — Monthly Operations Review"},
        {"type": "body", "text":
         "Complete in the last week of each month. Office manager and practice lead review together."},
        {"type": "numbered", "items": [
            "Review open action items from all weekly huddles this month. Anything older than 30 days must be resolved or formally parked.",
            "Review any task that escalated to practice lead — identify root cause and update the routing protocol if needed.",
            "Review team feedback log — any recurring friction or requests?",
            "Confirm all SOPs in active use are current (check dates, flag any outdated).",
            "Confirm supply and vendor contracts are current.",
            "Identify one workflow to improve next month.",
            "Draft next month's meeting rhythm and set recurring agenda items.",
        ]},

        {"type": "space", "size": 10},
        {"type": "subheading", "text": "QC Checklist C — New SOP or Template Adoption"},
        {"type": "body", "text":
         "Use this checklist any time a new SOP or template is introduced to the team."},
        {"type": "table",
         "headers": ["Step", "Owner", "Done?"],
         "colWidths": [280, 120, 100],
         "rows": [
             ["SOP/template drafted and reviewed by practice lead.", "Practice lead", ""],
             ["All affected team members notified.", "Office manager", ""],
             ["Training or walkthrough session completed.", "Office manager", ""],
             ["SOP filed in the shared documentation folder.", "Designated admin", ""],
             ["Old version archived (not deleted).", "Designated admin", ""],
             ["30-day check-in scheduled to review adoption.", "Office manager", ""],
         ]},
    ],
    FOOTER
)


print("All 3 full deliverable PDFs generated.")
print("Next step: create a ZIP with all three for the Complete AI Dentist SOP Library bundle.")
