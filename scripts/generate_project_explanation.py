#!/usr/bin/env python3
"""Render docs/project-explanation.md as a styled PDF using ReportLab."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted, HRFlowable

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "project-explanation.md"
OUT = ROOT / "docs" / "project-explanation.pdf"
NAVY = colors.HexColor("#10243A")
BLUE = colors.HexColor("#1769AA")
CYAN = colors.HexColor("#18A6A6")
PALE = colors.HexColor("#F3F7FA")
BORDER = colors.HexColor("#D5E0E8")
INK = colors.HexColor("#263746")
MUTED = colors.HexColor("#637485")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="GuideTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=24, leading=30, textColor=NAVY, alignment=TA_CENTER, spaceAfter=9))
styles.add(ParagraphStyle(name="GuideSub", parent=styles["Normal"], fontName="Helvetica", fontSize=10, leading=14, textColor=MUTED, alignment=TA_CENTER, spaceAfter=18))
styles.add(ParagraphStyle(name="H1Guide", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17, leading=22, textColor=NAVY, spaceBefore=8, spaceAfter=8, keepWithNext=True))
styles.add(ParagraphStyle(name="H2Guide", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=BLUE, spaceBefore=8, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name="BodyGuide", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.7, leading=12.2, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="BulletGuide", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=INK, leftIndent=13, firstLineIndent=-8, spaceAfter=3))
styles.add(ParagraphStyle(name="CodeGuide", parent=styles["Code"], fontName="Courier", fontSize=7.6, leading=10.5, textColor=NAVY, backColor=PALE, borderColor=BORDER, borderWidth=.5, borderPadding=6, leftIndent=5, rightIndent=5, spaceBefore=3, spaceAfter=7))
styles.add(ParagraphStyle(name="CellGuide", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.1, leading=9.1, textColor=INK))
styles.add(ParagraphStyle(name="CellBoldGuide", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.1, leading=9.1, textColor=INK))
styles.add(ParagraphStyle(name="HeadCellGuide", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.3, leading=9.2, textColor=colors.white))

def inline_markup(s):
    s = escape(s.strip())
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`(.+?)`', r'<font name="Courier-Bold">\1</font>', s)
    s = re.sub(r'\[(.+?)\]\((https?://[^ )]+)\)', r'<link href="\2" color="#1769AA">\1</link>', s)
    return s

def parse_table(lines):
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c or "-") for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return None
    width = 176 * mm
    n = max(len(r) for r in rows)
    colwidths = [width / n] * n
    data = []
    for ri, row in enumerate(rows):
        row += [""] * (n - len(row))
        style = "HeadCellGuide" if ri == 0 else "CellGuide"
        data.append([Paragraph(inline_markup(cell), styles[style]) for cell in row])
    t = Table(data, colWidths=colwidths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY), ("GRID",(0,0),(-1,-1),.35,BORDER),
        ("VALIGN",(0,0),(-1,-1),"TOP"), ("LEFTPADDING",(0,0),(-1,-1),5),
        ("RIGHTPADDING",(0,0),(-1,-1),5), ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,PALE]),
    ]))
    return t

def page_decor(canvas, doc):
    canvas.saveState()
    w, h = A4
    if doc.page > 1:
        canvas.setStrokeColor(BORDER)
        canvas.line(17*mm, h-14*mm, w-17*mm, h-14*mm)
        canvas.setFont("Helvetica-Bold", 7.5); canvas.setFillColor(NAVY)
        canvas.drawString(17*mm, h-10.5*mm, "INFORMATICA POWERCENTER | RETAIL DATA WAREHOUSE")
        canvas.setFont("Helvetica", 7.4); canvas.setFillColor(MUTED)
        canvas.drawRightString(w-17*mm, 9*mm, f"Project Guide | Page {doc.page}")
        canvas.line(17*mm, 13*mm, w-17*mm, 13*mm)
    canvas.restoreState()

def build():
    lines = SRC.read_text(encoding="utf-8").splitlines()
    story = []
    paragraph = []
    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            txt = " ".join(part.strip() for part in paragraph)
            story.append(Paragraph(inline_markup(txt), styles["BodyGuide"]))
            paragraph = []
    i = 0
    first_h1 = True
    in_code = False
    code_lines = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            flush_paragraph()
            if not in_code:
                in_code = True; code_lines = []
            else:
                story.append(Preformatted("\n".join(code_lines), styles["CodeGuide"]))
                in_code = False
            i += 1; continue
        if in_code:
            code_lines.append(line); i += 1; continue
        if not line.strip():
            flush_paragraph(); i += 1; continue
        if line.startswith("|"):
            flush_paragraph()
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i]); i += 1
            t = parse_table(table_lines)
            if t: story.extend([t, Spacer(1, 5)])
            continue
        if line.startswith("# "):
            flush_paragraph()
            title = line[2:].strip()
            if first_h1:
                story.extend([Spacer(1, 15*mm), Paragraph(inline_markup(title), styles["GuideTitle"]),
                              Paragraph("INFORMATICA POWERCENTER + POSTGRESQL | DATA ENGINEERING PORTFOLIO", styles["GuideSub"]),
                              HRFlowable(width="100%", thickness=1.3, color=CYAN), Spacer(1, 8)])
                first_h1 = False
            else:
                story.append(Paragraph(inline_markup(title), styles["H1Guide"]))
            i += 1; continue
        if line.startswith("## "):
            flush_paragraph(); story.append(Paragraph(inline_markup(line[3:]), styles["H2Guide"])); i += 1; continue
        if line.startswith("### "):
            flush_paragraph(); story.append(Paragraph(inline_markup(line[4:]), styles["Heading3"])); i += 1; continue
        if line.startswith("> "):
            flush_paragraph()
            quote = inline_markup(line[2:])
            story.append(Paragraph(quote, ParagraphStyle("QuoteTmp", parent=styles["BodyGuide"], leftIndent=10, rightIndent=10, borderColor=BORDER, borderWidth=.5, borderPadding=6, backColor=PALE)))
            i += 1; continue
        if line.startswith("- "):
            flush_paragraph()
            story.append(Paragraph("&bull; " + inline_markup(line[2:]), styles["BulletGuide"]))
            i += 1; continue
        if re.match(r"^\d+\.\s", line):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line), styles["BulletGuide"]))
            i += 1; continue
        paragraph.append(line)
        i += 1
    flush_paragraph()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=17*mm, rightMargin=17*mm, topMargin=19*mm, bottomMargin=18*mm,
                            title="Informatica PowerCenter Retail Data Warehouse ETL - Project Explanation",
                            author="Data Engineering Portfolio Guide")
    doc.build(story, onFirstPage=page_decor, onLaterPages=page_decor)
    print(f"Created {OUT} ({OUT.stat().st_size} bytes)")

if __name__ == "__main__":
    build()
