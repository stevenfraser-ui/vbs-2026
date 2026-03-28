from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem

md_path = Path("story/activity-ideas.md")
pdf_path = Path("story/activity-ideas.pdf")

text = md_path.read_text(encoding="utf-8")
lines = text.splitlines()

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H1Custom", parent=styles["Heading1"], spaceAfter=10))
styles.add(ParagraphStyle(name="H2Custom", parent=styles["Heading2"], spaceAfter=8))
styles.add(ParagraphStyle(name="BodyCustom", parent=styles["BodyText"], leading=14, spaceAfter=6))

story = []
list_buffer = []


def flush_list() -> None:
    if not list_buffer:
        return
    items = [ListItem(Paragraph(item, styles["BodyCustom"])) for item in list_buffer]
    story.append(ListFlowable(items, bulletType="bullet", leftIndent=18))
    story.append(Spacer(1, 0.08 * inch))
    list_buffer.clear()


for raw in lines:
    line = raw.strip()

    if not line:
        flush_list()
        story.append(Spacer(1, 0.08 * inch))
        continue

    if line.startswith("# "):
        flush_list()
        story.append(Paragraph(line[2:].strip(), styles["H1Custom"]))
        continue

    if line.startswith("## "):
        flush_list()
        story.append(Paragraph(line[3:].strip(), styles["H2Custom"]))
        continue

    if line.startswith("### "):
        flush_list()
        story.append(Paragraph(line[4:].strip(), styles["Heading3"]))
        continue

    if line.startswith("- ") or line.startswith("* "):
        list_buffer.append(line[2:].strip())
        continue

    flush_list()
    safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    story.append(Paragraph(safe, styles["BodyCustom"]))

flush_list()

doc = SimpleDocTemplate(
    str(pdf_path),
    pagesize=LETTER,
    leftMargin=0.85 * inch,
    rightMargin=0.85 * inch,
    topMargin=0.85 * inch,
    bottomMargin=0.85 * inch,
)
doc.build(story)

print(f"Created {pdf_path}")
