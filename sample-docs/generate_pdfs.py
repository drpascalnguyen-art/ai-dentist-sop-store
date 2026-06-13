"""
Generate sample PDFs for Lemon Squeezy approval reply.
Run from: /Users/pascalnguyen/Documents/New project/lemon-squeezy-store/sample-docs/
"""

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

BRAND_COLOR = colors.HexColor("#1a1a2e")
ACCENT_COLOR = colors.HexColor("#4361ee")
LIGHT_GRAY = colors.HexColor("#f8f8f8")
MID_GRAY = colors.HexColor("#666666")

def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("title", parent=base["Title"],
            fontSize=20, textColor=BRAND_COLOR, spaceAfter=6, leading=24),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"],
            fontSize=11, textColor=MID_GRAY, spaceAfter=20, leading=14),
        "h2": ParagraphStyle("h2", parent=base["Heading2"],
            fontSize=13, textColor=BRAND_COLOR, spaceBefore=16, spaceAfter=6, leading=16),
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
        if section["type"] == "heading":
            story.append(Paragraph(section["text"], s["h2"]))
        elif section["type"] == "body":
            story.append(Paragraph(section["text"], s["body"]))
        elif section["type"] == "bullet":
            for item in section["items"]:
                story.append(Paragraph(f"• {item}", s["bullet"]))
            story.append(Spacer(1, 4))
        elif section["type"] == "numbered":
            for i, item in enumerate(section["items"], 1):
                story.append(Paragraph(f"{i}. {item}", s["bullet"]))
            story.append(Spacer(1, 4))
        elif section["type"] == "table":
            tdata = [section["headers"]] + section["rows"]
            t = Table(tdata, hAlign="LEFT", colWidths=section.get("colWidths"))
            t.setStyle(TableStyle([
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
            story.append(t)
            story.append(Spacer(1, 8))
        elif section["type"] == "notice":
            story.append(Paragraph(section["text"], s["notice"]))
        elif section["type"] == "space":
            story.append(Spacer(1, section.get("size", 8)))

    story.append(Spacer(1, 24))
    story.append(Paragraph(footer_line, s["footer"]))

    doc.build(story)
    print(f"Generated: {filename}")


FOOTER = "© 2026 Dr. Pascal Nguyen, DMD, NMD / PJN Dental. Educational and operational resource — not clinical, legal, or compliance advice."


# ─── PDF 1: SOP Starter Pack ────────────────────────────────────────────────

build_pdf(
    "ai-dentist-sop-starter-pack-sample.pdf",
    "AI Dentist SOP Starter Pack",
    "Sample — AI Use-Case Intake SOP",
    [
        {"type": "notice", "text":
         "This sample demonstrates the style and scope of the digital SOP templates included in the AI Dentist SOP Starter Pack."},
        {"type": "heading", "text": "AI Use-Case Intake SOP"},
        {"type": "body", "text":
         "Purpose: Create a simple review process before a dental team uses an AI tool for administrative, marketing, or internal workflow tasks."},
        {"type": "heading", "text": "Approved Use Cases"},
        {"type": "bullet", "items": [
            "Drafting internal checklists from already-approved practice procedures.",
            "Summarizing non-patient-specific meeting notes.",
            "Creating first drafts of educational content for human review.",
            "Organizing recurring admin tasks into templates.",
        ]},
        {"type": "heading", "text": "Not Approved Without Separate Review"},
        {"type": "bullet", "items": [
            "Entering patient health information into unapproved tools.",
            "Generating diagnosis, treatment, medication, or clinical instructions.",
            "Publishing patient-facing content without human review.",
            "Representing AI output as final professional advice.",
        ]},
        {"type": "heading", "text": "Team Checklist"},
        {"type": "numbered", "items": [
            "Confirm the task does not require protected health information.",
            "Select an approved tool and approved prompt template.",
            "Review output for accuracy, tone, and compliance boundaries.",
            "Assign a human owner for final approval.",
            "Save the final SOP or document in the approved practice location.",
        ]},
        {"type": "heading", "text": "Human Review Standard"},
        {"type": "body", "text":
         "Every AI-assisted output must be reviewed by a qualified team member before it is used in operations, training, or patient-facing communication."},
    ],
    FOOTER
)


# ─── PDF 2: Marketing Prompt Pack ────────────────────────────────────────────

build_pdf(
    "ai-dental-marketing-prompt-pack-sample.pdf",
    "AI Dental Marketing Prompt Pack",
    "Sample — Educational Post Draft Prompt",
    [
        {"type": "notice", "text":
         "This sample demonstrates the style and scope of the marketing prompt templates included in the AI Dental Marketing Prompt Pack."},
        {"type": "heading", "text": "Educational Post Draft Prompt"},
        {"type": "body", "text":
         "Use this prompt for first-draft educational content. Do not publish without review."},
        {"type": "body", "text":
         'Write a patient-friendly educational post about [TOPIC] for a dental practice audience.\n\n'
         'Requirements: Keep the tone clear, warm, and non-alarming. Avoid diagnosis, treatment promises, or guaranteed outcomes. '
         'Use "may," "can," and "is associated with" when appropriate. '
         'Include a reminder to discuss individual concerns with a qualified dental or medical professional. '
         'End with a gentle call to action to schedule a consultation or ask a question.'},
        {"type": "heading", "text": "Human Review Checklist"},
        {"type": "bullet", "items": [
            "No diagnosis claim.",
            "No cure, reversal, or guaranteed outcome.",
            "No patient-specific advice.",
            "No unsupported clinical claim.",
            "No unapproved before-and-after promise.",
            "Clear distinction between education and individualized care.",
        ]},
        {"type": "heading", "text": "Example Topic List"},
        {"type": "bullet", "items": [
            "Why gums can bleed and when to ask a dentist.",
            "How airway and sleep can relate to dental health.",
            "What patients should know before an implant consultation.",
            "How dental teams evaluate biological dentistry questions.",
        ]},
    ],
    FOOTER
)


# ─── PDF 3: Clinical Admin Workflow SOP Bundle ───────────────────────────────

build_pdf(
    "clinical-admin-workflow-sop-bundle-sample.pdf",
    "Clinical Admin Workflow SOP Bundle",
    "Sample — Meeting Notes to Action Register SOP",
    [
        {"type": "notice", "text":
         "This sample demonstrates the style and scope of the administrative workflow templates included in the Clinical Admin Workflow SOP Bundle."},
        {"type": "heading", "text": "Meeting Notes To Action Register SOP"},
        {"type": "body", "text":
         "Purpose: Turn dental team meeting notes into clear tasks with owners, due dates, and next actions."},
        {"type": "heading", "text": "Inputs"},
        {"type": "bullet", "items": [
            "Meeting date.",
            "Attendees.",
            "Discussion notes.",
            "Decisions made.",
            "Open loops.",
            "Follow-up owners.",
        ]},
        {"type": "heading", "text": "Output Format"},
        {"type": "table",
         "headers": ["Action", "Owner", "Due Date", "Next Action", "Status"],
         "colWidths": [130, 90, 70, 130, 50],
         "rows": [
             ["Document ledger posting procedure", "Office lead", "Friday",
              "Confirm final steps and training gaps", "Open"],
             ["Review schedule bottlenecks", "Doctor + office lead", "Tuesday",
              "Identify top two appointment types running long", "Open"],
         ]},
        {"type": "heading", "text": "Quality Standard"},
        {"type": "body", "text":
         "Every action must have one directly responsible owner. If an item has multiple contributors, "
         "list one owner and name the supporting roles in the notes."},
        {"type": "heading", "text": "Review Rhythm"},
        {"type": "bullet", "items": [
            "Review open tasks weekly.",
            "Close tasks only when the output is documented or assigned to a new workflow.",
            "Move unclear items into a parking lot instead of letting them disappear.",
        ]},
    ],
    FOOTER
)

print("All 3 sample PDFs generated successfully.")
