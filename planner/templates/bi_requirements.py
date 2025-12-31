from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import datetime
from ..core.constants import (
    IPAD_PRO_11_LANDSCAPE, BACKGROUND_COLOR, CARD_COLOR, LABEL_COLOR, 
    SECONDARY_LABEL, SEPARATOR_COLOR, SYSTEM_BLUE, SYSTEM_GRAY, SYSTEM_GRAY_2,
    MONTH_COLORS
)
from ..core.utils import draw_icon, draw_apple_tab

def draw_bi_requirements_page(c, W, H):
    margin = 20 * mm
    
    # Section Colors
    color_questions = MONTH_COLORS[2]  # Sage Green
    color_notes = MONTH_COLORS[4]      # Muted Steel Blue
    
    c.saveState()
    
    # Background
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Header
    header_y = H - 22 * mm
    c.setFillColor(LABEL_COLOR)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(margin, header_y, "BI Requirements")
    
    # Project Info Bar (Top Right)
    c.setFont("Helvetica", 10)
    c.setFillColor(SYSTEM_GRAY)
    c.drawRightString(W - margin, header_y + 6*mm, f"Date: ________________")
    c.drawRightString(W - margin, header_y, f"Stakeholder: ________________")

    info_y = header_y - 15 * mm
    c.setFont("Helvetica", 12)
    c.drawString(margin, info_y, f"Project: ________________________________________________")

    # Layout Constants
    top_y = info_y - 15 * mm
    bottom_y = 20 * mm
    available_h = top_y - bottom_y
    col_gap = 10 * mm
    left_col_w = (W - 2*margin - col_gap) * 0.45
    right_col_w = (W - 2*margin - col_gap) * 0.55
    
    x1 = margin
    x2 = margin + left_col_w + col_gap

    # --- Left Column: Discovery Questions ---
    c.setFillColor(color_questions)
    c.setFont("Helvetica-Bold", 13)
    draw_icon(c, "discovery", x1 + 1*mm, top_y + 1.5*mm, 4.5*mm, color_questions)
    c.drawString(x1 + 7*mm, top_y + 2.0*mm, "Discovery Questions")
    
    # Box for questions
    c.setFillColor(CARD_COLOR)
    c.roundRect(x1, bottom_y, left_col_w, available_h, 5*mm, fill=1, stroke=0)
    
    questions = [
        "What business decision will this data drive?",
        "Why is this important to the business?",
        "How are you currently getting this data?",
        "Overview vs. Deep Dive granularity?",
        "Core KPIs & how they are calculated?",
        "Dimensions needed (filters/slicing)?",
        "Compliance/Legal/GDPR implications?",
        "Does refresh align with data updates?",
        "What other departments use this data?",
        "What does 'Success' look like?",
    ]
    
    curr_q_y = top_y - 8 * mm
    c.setFont("Helvetica", 8.5)
    c.setFillColor(SECONDARY_LABEL)
    
    q_spacing = (available_h - 10*mm) / len(questions)
    
    for q in questions:
        # Bullet/Checkbox
        c.setStrokeColor(color_questions)
        c.setLineWidth(0.6)
        c.rect(x1 + 5*mm, curr_q_y - 0.5*mm, 2.5*mm, 2.5*mm, fill=0, stroke=1)
        
        # Question text
        c.drawString(x1 + 10*mm, curr_q_y, q)
        
        curr_q_y -= q_spacing

    # --- Right Column: Notes ---
    c.setFillColor(color_notes)
    c.setFont("Helvetica-Bold", 13)
    draw_icon(c, "notes", x2 + 1*mm, top_y + 1.5*mm, 4.5*mm, color_notes)
    c.drawString(x2 + 7*mm, top_y + 2.0*mm, "Notes")
    
    # Box for notes
    c.setFillColor(CARD_COLOR)
    c.roundRect(x2, bottom_y, right_col_w, available_h, 5*mm, fill=1, stroke=0)
    
    # Dotted Grid
    c.setFillColor(SEPARATOR_COLOR)
    dot_spacing = 5 * mm
    dot_size = 0.25 * mm
    
    grid_left = x2 + 5*mm
    grid_right = x2 + right_col_w - 5*mm
    grid_top = top_y - 5*mm
    grid_bottom = bottom_y + 5*mm
    
    curr_dot_y = grid_top
    while curr_dot_y >= grid_bottom:
        curr_dot_x = grid_left
        while curr_dot_x <= grid_right:
            c.circle(curr_dot_x, curr_dot_y, dot_size, fill=1, stroke=0)
            curr_dot_x += dot_spacing
        curr_dot_y -= dot_spacing

    c.restoreState()

def draw_full_notes_page(c, W, H):
    margin = 20 * mm
    
    c.saveState()
    
    # Background
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Layout Constants
    top_y = H - margin
    bottom_y = margin
    available_h = top_y - bottom_y
    
    # Box for notes (Full Page)
    c.setFillColor(CARD_COLOR)
    c.roundRect(margin, bottom_y, W - 2*margin, available_h, 5*mm, fill=1, stroke=0)
    
    # Dotted Grid
    c.setFillColor(SEPARATOR_COLOR)
    dot_spacing = 5 * mm
    dot_size = 0.25 * mm
    
    grid_left = margin + 5*mm
    grid_right = W - margin - 5*mm
    grid_top = top_y - 5*mm
    grid_bottom = bottom_y + 5*mm
    
    curr_dot_y = grid_top
    while curr_dot_y >= grid_bottom:
        curr_dot_x = grid_left
        while curr_dot_x <= grid_right:
            c.circle(curr_dot_x, curr_dot_y, dot_size, fill=1, stroke=0)
            curr_dot_x += dot_spacing
        curr_dot_y -= dot_spacing

    c.restoreState()

def generate_bi_requirements_pdf(output_path):
    W, H = IPAD_PRO_11_LANDSCAPE
    c = canvas.Canvas(output_path, pagesize=(W, H))
    
    # Page 1: Requirements Checklist
    draw_bi_requirements_page(c, W, H)
    c.showPage()
    
    # Page 2: Full Notes
    draw_full_notes_page(c, W, H)
    c.showPage()
        
    c.save()
