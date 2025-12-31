from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import datetime
from .generator import (
    IPAD_PRO_11_LANDSCAPE, BACKGROUND_COLOR, CARD_COLOR, LABEL_COLOR, 
    SEPARATOR_COLOR, SYSTEM_BLUE, SYSTEM_GRAY, SYSTEM_GRAY_2,
    draw_icon, draw_apple_tab, MONTH_COLORS
)

def draw_centered_rows(c, x, y_top, w, h, num_rows, row_h, draw_row_func):
    """
    Helper to draw a block of rows centered vertically within a box.
    y_top is the top edge of the box.
    h is the total height of the box.
    """
    total_content_h = num_rows * row_h
    # Vertical margin to center the block of rows
    margin_y = (h - total_content_h) / 2
    
    for i in range(num_rows):
        # Top of this specific row
        row_top = y_top - margin_y - (i * row_h)
        # Bottom of this specific row
        row_bottom = row_top - row_h
        # Center of this specific row
        row_center = row_top - (row_h / 2)
        
        draw_row_func(c, x, row_top, row_bottom, row_center, w, row_h, i)

def draw_meeting_notes_page(c, W, H):
    margin = 20 * mm
    
    # Section Colors
    color_details = MONTH_COLORS[0]    # Muted Rose
    color_attendees = MONTH_COLORS[2]  # Sage Green
    color_agenda = MONTH_COLORS[1]     # Muted Terracotta
    color_decisions = MONTH_COLORS[4]  # Muted Steel Blue
    color_action = MONTH_COLORS[5]     # Muted Lavender
    
    c.saveState()
    
    # Background
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Header
    header_y = H - 22 * mm
    c.setFillColor(LABEL_COLOR)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(margin, header_y, "Meeting Notes")
    
    # Project Info Bar (Top Right)
    c.setFont("Helvetica", 10)
    c.setFillColor(SYSTEM_GRAY)
    c.drawRightString(W - margin, header_y + 6*mm, f"Date: ________________")

    # Layout
    col_gap = 10 * mm
    left_col_w = (W - 2*margin - col_gap) * 0.40
    right_col_w = (W - 2*margin - col_gap) * 0.60
    
    top_y = H - 40 * mm
    bottom_y = 15 * mm
    available_h = top_y - bottom_y
    
    x1 = margin
    x2 = margin + left_col_w + col_gap
    
    # Vertical spacing between boxes
    box_gap = 10 * mm
    
    # --- Left Column ---
    
    # 1. Attendees
    attendees_h = 55 * mm
    # Title
    c.setFillColor(color_attendees)
    c.setFont("Helvetica-Bold", 13)
    draw_icon(c, "important", x1 + 1*mm, top_y + 1.5*mm, 4.5*mm, color_attendees)
    c.drawString(x1 + 7*mm, top_y + 2.0*mm, "Attendees")
    # Box
    c.setFillColor(CARD_COLOR)
    c.roundRect(x1, top_y - attendees_h, left_col_w, attendees_h, 5*mm, fill=1, stroke=0)
    
    def draw_attendees_row(c, x, r_top, r_bottom, r_center, w, rh, i):
        c.setStrokeColor(SEPARATOR_COLOR)
        c.setLineWidth(0.5)
        c.line(x + 5*mm, r_bottom + 2*mm, x + w - 5*mm, r_bottom + 2*mm)

    draw_centered_rows(c, x1, top_y, left_col_w, attendees_h, 6, 8*mm, draw_attendees_row)

    # 2. Agenda
    agenda_top_y = top_y - attendees_h - box_gap
    agenda_h = agenda_top_y - bottom_y
    # Title
    c.setFillColor(color_agenda)
    c.setFont("Helvetica-Bold", 13)
    draw_icon(c, "overview", x1 + 1*mm, agenda_top_y + 1.5*mm, 4.5*mm, color_agenda)
    c.drawString(x1 + 7*mm, agenda_top_y + 2.0*mm, "Agenda")
    # Box
    c.setFillColor(CARD_COLOR)
    c.roundRect(x1, agenda_top_y - agenda_h, left_col_w, agenda_h, 5*mm, fill=1, stroke=0)
    
    def draw_agenda_row(c, x, r_top, r_bottom, r_center, w, rh, i):
        c.setStrokeColor(SEPARATOR_COLOR)
        c.setLineWidth(0.5)
        c.line(x + 12*mm, r_bottom + 2*mm, x + w - 5*mm, r_bottom + 2*mm)
        # Checkbox
        c.setStrokeColor(color_agenda)
        c.setLineWidth(0.8)
        c.rect(x + 5*mm, r_center - 2*mm, 4*mm, 4*mm, fill=0, stroke=1)

    num_agenda_rows = int((agenda_h - 4*mm) / (8*mm))
    if num_agenda_rows < 1: num_agenda_rows = 1
    draw_centered_rows(c, x1, agenda_top_y, left_col_w, agenda_h, num_agenda_rows, 8*mm, draw_agenda_row)

    # --- Right Column ---
    
    # 1. Action Items
    action_h = attendees_h # Align with Attendees
    # Title
    c.setFillColor(color_action)
    c.setFont("Helvetica-Bold", 13)
    draw_icon(c, "todo", x2 + 1*mm, top_y + 1.5*mm, 4.5*mm, color_action)
    c.drawString(x2 + 7*mm, top_y + 2.0*mm, "Action Items")
    # Box
    c.setFillColor(CARD_COLOR)
    c.roundRect(x2, top_y - action_h, right_col_w, action_h, 5*mm, fill=1, stroke=0)
    
    def draw_action_row(c, x, r_top, r_bottom, r_center, w, rh, i):
        c.setStrokeColor(SEPARATOR_COLOR)
        c.setLineWidth(0.5)
        c.line(x + 10*mm, r_bottom + 2*mm, x + w - 5*mm, r_bottom + 2*mm)
        # Bullet
        c.setFillColor(color_action)
        c.circle(x + 7*mm, r_center, 1*mm, fill=1, stroke=0)

    num_action_rows = int((action_h - 4*mm) / (9*mm))
    draw_centered_rows(c, x2, top_y, right_col_w, action_h, num_action_rows, 9*mm, draw_action_row)

    # 2. Key Decisions
    decisions_top_y = top_y - action_h - box_gap
    decisions_h = decisions_top_y - bottom_y
    # Title
    c.setFillColor(color_decisions)
    c.setFont("Helvetica-Bold", 13)
    draw_icon(c, "priorities", x2 + 1*mm, decisions_top_y + 1.5*mm, 4.5*mm, color_decisions)
    c.drawString(x2 + 7*mm, decisions_top_y + 2.0*mm, "Key Decisions")
    # Box
    c.setFillColor(CARD_COLOR)
    c.roundRect(x2, decisions_top_y - decisions_h, right_col_w, decisions_h, 5*mm, fill=1, stroke=0)
    
    def draw_decision_row(c, x, r_top, r_bottom, r_center, w, rh, i):
        c.setStrokeColor(SEPARATOR_COLOR)
        c.setLineWidth(0.5)
        c.line(x + 10*mm, r_bottom + 2*mm, x + w - 5*mm, r_bottom + 2*mm)
        # Star/Bullet
        c.setFillColor(color_decisions)
        c.circle(x + 7*mm, r_center, 1*mm, fill=1, stroke=0)

    num_decision_rows = int((decisions_h - 4*mm) / (9*mm))
    draw_centered_rows(c, x2, decisions_top_y, right_col_w, decisions_h, num_decision_rows, 9*mm, draw_decision_row)

    c.restoreState()

def draw_full_meeting_notes_page(c, W, H):
    margin = 20 * mm
    color_notes = MONTH_COLORS[4]      # Muted Steel Blue
    
    c.saveState()
    
    # Background
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Header
    header_y = H - 22 * mm
    c.setFillColor(LABEL_COLOR)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(margin, header_y, "Meeting Notes")
    
    # Layout Constants
    top_y = H - 40 * mm
    bottom_y = 15 * mm
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

def generate_meeting_notes_pdf(out_path):
    W, H = IPAD_PRO_11_LANDSCAPE
    c = canvas.Canvas(out_path, pagesize=(W, H))
    
    # Page 1: Summary
    draw_meeting_notes_page(c, W, H)
    c.showPage()
    
    # Page 2: Full Notes
    draw_full_meeting_notes_page(c, W, H)
    c.showPage()
    
    c.save()
