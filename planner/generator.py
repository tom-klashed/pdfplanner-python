from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import calendar
import os
from datetime import datetime, timedelta

# iPad Pro 11" Landscape: 2388 x 1668 pixels @ 264 ppi
# 2388 / 264 * 72 = 651.27 pts
# 1668 / 264 * 72 = 454.91 pts
IPAD_PRO_11_LANDSCAPE = (651.27, 454.91)

# Apple System Colors (Muted/Pastel Palette)
SYSTEM_BLUE = colors.HexColor("#5E97F6")
SYSTEM_RED = colors.HexColor("#EF9A9A")
SYSTEM_GRAY = colors.HexColor("#8E8E93")
SYSTEM_GRAY_2 = colors.HexColor("#AEAEB2")
SYSTEM_GRAY_3 = colors.HexColor("#C7C7CC")
SYSTEM_GRAY_4 = colors.HexColor("#D1D1D6")
SYSTEM_GRAY_5 = colors.HexColor("#E5E5EA")
SYSTEM_GRAY_6 = colors.HexColor("#F2F0E6") # Lighter cream for cards
LABEL_COLOR = colors.HexColor("#1D1D1F")
SECONDARY_LABEL = colors.HexColor("#6E6E73")
TERTIARY_LABEL = colors.HexColor("#86868B")
SEPARATOR_COLOR = colors.HexColor("#D2D2D7")
BACKGROUND_COLOR = colors.HexColor("#E6E3D2") # Warm Cream Background
CARD_COLOR = SYSTEM_GRAY_6

# Muted "Earth-Tone" Pastel Palette for Monthly Themes
MONTH_COLORS = [
    colors.HexColor("#D48C88"), # Jan - Muted Rose
    colors.HexColor("#D9A07E"), # Feb - Muted Terracotta
    colors.HexColor("#A3B18A"), # Mar - Sage Green
    colors.HexColor("#84A59D"), # Apr - Muted Teal
    colors.HexColor("#90A8C3"), # May - Muted Steel Blue
    colors.HexColor("#A594B1"), # Jun - Muted Lavender
    colors.HexColor("#8E7D9E"), # Jul - Dusty Purple
    colors.HexColor("#B5838D"), # Aug - Dusty Rose
    colors.HexColor("#E5989B"), # Sep - Muted Coral
    colors.HexColor("#DDBEA9"), # Oct - Sand
    colors.HexColor("#A5A5A5"), # Nov - Muted Gray
    colors.HexColor("#6B705C"), # Dec - Olive
]

# Icon Mapping
ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons")
ICONS = {
    "todo": "add_task_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "priorities": "bookmark_star_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "notes": "event_list_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "schedule": "schedule_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "home": "today_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "important": "notification_important_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "goals": "bookmark_check_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "calendar": "calendar_month_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "overview": "date_range_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg"
}

def draw_icon(c, icon_key, x, y, size, color=None):
    """Draws and colorizes an SVG icon."""
    if icon_key not in ICONS:
        return
    
    path = os.path.join(ICON_DIR, ICONS[icon_key])
    if not os.path.exists(path):
        return
        
    drawing = svg2rlg(path)
    
    # Scale the drawing
    scale = size / drawing.width
    drawing.width *= scale
    drawing.height *= scale
    drawing.scale(scale, scale)
    
    # Colorize the drawing
    if color:
        def colorize(obj):
            if hasattr(obj, 'fillColor'):
                obj.fillColor = color
            if hasattr(obj, 'strokeColor'):
                obj.strokeColor = color
            if hasattr(obj, 'contents'):
                for child in obj.contents:
                    colorize(child)
        colorize(drawing)
        
    renderPDF.draw(drawing, c, x, y)

def is_dark_color(color):
    """Simple brightness check to decide text color."""
    # Get RGB values (0-1)
    r, g, b = color.red, color.green, color.blue
    # Standard luminance formula
    luminance = (0.299 * r + 0.587 * g + 0.114 * b)
    return luminance < 0.6

def draw_side_tabs(c, W, H, current_month=None):
    """Draws vertical month tabs on the right side of the page."""
    tab_w = 8 * mm
    tab_h = (H - 40*mm) / 12
    x = W - tab_w + 2*mm # Slightly overlapping edge for "tab" look
    
    c.saveState()
    for i in range(12):
        m = i + 1
        y = H - 30*mm - (i+1)*tab_h
        
        color = MONTH_COLORS[i]
        c.setFillColor(color)
        
        # If active, make it pop out more
        is_active = (m == current_month)
        draw_x = x - (4*mm if is_active else 0)
        draw_w = tab_w + (4*mm if is_active else 0)
        
        # Draw Tab with rounded left corners
        c.roundRect(draw_x, y, draw_w, tab_h - 0.5*mm, 2*mm, fill=1, stroke=0)
        
        # Month Label (Vertical Text)
        c.saveState()
        # Choose text color based on background brightness
        if is_dark_color(color):
            c.setFillColor(colors.white)
            c.setFillAlpha(0.9)
        else:
            c.setFillColor(LABEL_COLOR)
            c.setFillAlpha(0.8)
            
        c.setFont("Helvetica-Bold", 7)
        # Rotate text for vertical tab
        c.translate(draw_x + 3*mm, y + tab_h/2)
        c.rotate(90)
        c.drawCentredString(0, -1*mm, calendar.month_abbr[m].upper())
        c.restoreState()
        
        # Link to Monthly Page
        c.linkRect("", f"Month_{m}", (draw_x, y, W, y + tab_h), Border='[0 0 0]')
        
    c.restoreState()

def draw_home_button(c, W, H, margin, color=LABEL_COLOR):
    """Draws a subtle Home button in the top right."""
    btn_w = 25 * mm
    btn_h = 9 * mm
    x = W - margin - btn_w
    y = H - 22 * mm
    
    c.saveState()
    c.setFillColor(CARD_COLOR)
    c.roundRect(x, y, btn_w, btn_h, 2.5*mm, fill=1, stroke=0)
    
    c.setStrokeColor(SEPARATOR_COLOR)
    c.setLineWidth(0.1)
    c.roundRect(x, y, btn_w, btn_h, 2.5*mm, fill=0, stroke=1)
    
    # Icon
    draw_icon(c, "home", x + 3*mm, y + 2.2*mm, 4.5*mm, color)
    
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + 9*mm, y + btn_h/2 - 1.2*mm, "Home")
    
    c.linkRect("", "Cover", (x, y, x + btn_w, y + btn_h), Border='[0 0 0]')
    c.restoreState()

def draw_apple_tab(c, x, y, w, h, text, active=False, destination=None, color=LABEL_COLOR, icon_key=None):
    """Draws a native-looking iPadOS segmented control or button with optional hyperlink."""
    c.saveState()
    
    if active:
        c.setFillColor(color)
        c.roundRect(x, y, w, h, 2.5*mm, fill=1, stroke=0)
        text_color = colors.white
    else:
        c.setFillColor(CARD_COLOR)
        c.roundRect(x, y, w, h, 2.5*mm, fill=1, stroke=0)
        text_color = color
    
    c.setFillAlpha(1.0)
    # Subtle border for inactive tabs
    if not active:
        c.setStrokeColor(SEPARATOR_COLOR)
        c.setLineWidth(0.1)
        c.roundRect(x, y, w, h, 2.5*mm, fill=0, stroke=1)

    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", 10)
    
    if icon_key:
        draw_icon(c, icon_key, x + 3*mm, y + 2.2*mm, 4.5*mm, text_color)
        c.drawString(x + 9*mm, y + h/2 - 1.2*mm, text)
    else:
        c.drawCentredString(x + w/2, y + h/2 - 1.2*mm, text)
    
    if destination:
        # Create the clickable link area
        c.linkRect("", destination, (x, y, x+w, y+h), Border='[0 0 0]')
        
    c.restoreState()

def draw_yearly_tracker(c, year, W, H):
    margin = 20 * mm
    c.saveState()
    
    # Background
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Header
    c.setFont("Helvetica-Bold", 34)
    c.setFillColor(LABEL_COLOR)
    c.drawString(margin, H - 22*mm, f"{year}")
    c.setFont("Helvetica", 34)
    c.drawString(margin + c.stringWidth(f"{year} ", "Helvetica-Bold", 34), H - 22*mm, "Tracker")
    
    # Side Tabs
    draw_side_tabs(c, W, H)
    
    # Navigation Tabs
    tab_w = 32 * mm
    gap = 3 * mm
    r_margin = 15 * mm
    draw_apple_tab(c, W - r_margin - tab_w*3 - gap*2, H - 22*mm, tab_w, 9*mm, "Calendar", destination="YearlySummary", icon_key="calendar")
    draw_apple_tab(c, W - r_margin - tab_w*2 - gap, H - 22*mm, tab_w, 9*mm, "Summary", destination="SixMonth_1", icon_key="overview")
    draw_apple_tab(c, W - r_margin - tab_w, H - 22*mm, tab_w, 9*mm, "Tracker", active=True, destination="YearlyTracker", icon_key="goals")

    # Legend / Key at Top
    legend_y = H - 48*mm
    legend_x = margin + 15*mm
    grid_w_full = W - margin - legend_x - 10*mm
    item_w = grid_w_full / 4
    
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(SECONDARY_LABEL)
    c.drawString(legend_x, legend_y + 8*mm, "TRACKING KEY")
    
    for i in range(4):
        lx = legend_x + i*item_w
        # Quadrant Icon (Base Box)
        c.setStrokeColor(SECONDARY_LABEL)
        c.setStrokeAlpha(0.4)
        c.setLineWidth(0.15)
        c.roundRect(lx, legend_y + 1*mm, 4*mm, 4*mm, 0.5*mm, stroke=1, fill=0)
        
        # Inner lines for legend box to match grid
        c.line(lx + 2*mm, legend_y + 1*mm, lx + 2*mm, legend_y + 5*mm)
        c.line(lx, legend_y + 3*mm, lx + 4*mm, legend_y + 3*mm)
        
        # Fill the specific quadrant for this habit with a light shade
        c.setFillColor(SYSTEM_GRAY_4)
        c.setFillAlpha(0.3)
        if i == 0: # Top Left
            c.rect(lx, legend_y + 3*mm, 2*mm, 2*mm, fill=1, stroke=0)
        elif i == 1: # Top Right
            c.rect(lx + 2*mm, legend_y + 3*mm, 2*mm, 2*mm, fill=1, stroke=0)
        elif i == 2: # Bottom Left
            c.rect(lx, legend_y + 1*mm, 2*mm, 2*mm, fill=1, stroke=0)
        elif i == 3: # Bottom Right
            c.rect(lx + 2*mm, legend_y + 1*mm, 2*mm, 2*mm, fill=1, stroke=0)
        c.setFillAlpha(1.0)
        c.setStrokeAlpha(1.0)
        
        # Line for user to write
        c.setStrokeColor(SEPARATOR_COLOR)
        c.line(lx + 6*mm, legend_y + 1*mm, lx + item_w - 5*mm, legend_y + 1*mm)

    # Grid Setup
    grid_x = margin + 15*mm
    grid_y = H - 58*mm
    grid_w = grid_w_full
    grid_h = grid_y - 15*mm
    
    cell_w = grid_w / 31
    cell_h = grid_h / 12
    
    # Day Labels (1-31)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(SECONDARY_LABEL)
    for d in range(1, 32):
        c.drawCentredString(grid_x + (d-0.5)*cell_w, grid_y + 2*mm, str(d))
        
    for m in range(1, 13):
        my = grid_y - m*cell_h
        month_color = MONTH_COLORS[m-1]
        
        # Month Label
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(month_color)
        c.drawRightString(grid_x - 2*mm, my + cell_h/2 - 1*mm, calendar.month_abbr[m].upper())
        
        for d in range(1, 32):
            mx = grid_x + (d-1)*cell_w
            
            try:
                dt = datetime(year, m, d)
                is_weekend = dt.weekday() >= 5
                
                # Cell Background
                c.setStrokeColor(SECONDARY_LABEL)
                c.setStrokeAlpha(0.4)
                c.setLineWidth(0.15)
                if is_weekend:
                    c.setFillColor(colors.HexColor("#EBE8D8"))
                else:
                    c.setFillColor(CARD_COLOR)
                
                c.roundRect(mx + 0.4*mm, my + 0.4*mm, cell_w - 0.8*mm, cell_h - 0.8*mm, 0.5*mm, fill=1, stroke=1)
                
                # Quadrant Split (Revolutionary System)
                # Vertical line
                c.line(mx + cell_w/2, my + 0.4*mm, mx + cell_w/2, my + cell_h - 0.4*mm)
                # Horizontal line
                c.line(mx + 0.4*mm, my + cell_h/2, mx + cell_w - 0.4*mm, my + cell_h/2)
                c.setStrokeAlpha(1.0)
                
                # Link to Daily Page
                c.linkRect("", f"Day_{year}_{m}_{d}", (mx, my, mx + cell_w, my + cell_h), Border='[0 0 0]')
                
            except ValueError:
                pass
                
    c.restoreState()

def draw_cover(c, W, H, title):
    c.saveState()
    # Minimalist Apple Cover
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    c.setFillColor(LABEL_COLOR)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W / 2, H / 2 + 25*mm, "")
    
    c.setFont("Helvetica-Bold", 72)
    c.drawCentredString(W / 2, H / 2 - 5*mm, title)
    
    c.setFillColor(SECONDARY_LABEL)
    c.setFont("Helvetica", 24)
    c.drawCentredString(W / 2, H / 2 - 20*mm, "PLANNER")
    
    # Use a pastel accent from the palette
    c.setStrokeColor(MONTH_COLORS[0])
    c.setLineWidth(1.5)
    c.line(W/2 - 20*mm, H/2 - 30*mm, W/2 + 20*mm, H/2 - 30*mm)
    c.restoreState()

def draw_summary_page(c, year, W, H):
    margin = 20 * mm
    c.saveState()
    
    # Background
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Header
    c.setFont("Helvetica-Bold", 34)
    c.setFillColor(LABEL_COLOR)
    c.drawString(margin, H - 22*mm, f"{year}")
    c.setFont("Helvetica", 34)
    c.drawString(margin + c.stringWidth(f"{year} ", "Helvetica-Bold", 34), H - 22*mm, "Calendar")
    
    # Side Tabs
    draw_side_tabs(c, W, H)
    
    # Navigation Tabs (Top Right)
    tab_w = 32 * mm
    gap = 3 * mm
    r_margin = 15 * mm
    draw_apple_tab(c, W - r_margin - tab_w*3 - gap*2, H - 22*mm, tab_w, 9*mm, "Calendar", active=True, destination="YearlySummary", icon_key="calendar")
    draw_apple_tab(c, W - r_margin - tab_w*2 - gap, H - 22*mm, tab_w, 9*mm, "Summary", destination="SixMonth_1", icon_key="overview")
    draw_apple_tab(c, W - r_margin - tab_w, H - 22*mm, tab_w, 9*mm, "Tracker", destination="YearlyTracker", icon_key="goals")
    
    # Grid Setup (4 cols x 3 rows)
    grid_top = H - 40*mm
    grid_bottom = 15*mm
    grid_w = W - 2*margin
    grid_h = grid_top - grid_bottom
    
    cell_w = grid_w / 4
    cell_h = grid_h / 3
    
    cal = calendar.Calendar(firstweekday=0)
    for m in range(1, 13):
        col = (m-1) % 4
        row = (m-1) // 4
        x = margin + col * cell_w
        y = grid_top - row * cell_h
        
        # Month Name (Clickable)
        c.setFont("Helvetica-Bold", 12)
        month_color = MONTH_COLORS[m-1]
        c.setFillColor(month_color)
        month_name = calendar.month_name[m]
        c.drawString(x + 5*mm, y - 6*mm, month_name)
        # Link to Monthly Page
        c.linkRect("", f"Month_{m}", (x + 5*mm, y - 8*mm, x + 5*mm + c.stringWidth(month_name, "Helvetica-Bold", 12), y), Border='[0 0 0]')
        
        # Mini Calendar
        mini_w = cell_w - 10*mm
        mini_x = x + 5*mm
        mini_y = y - 12*mm
        
        # Day Headers
        c.setFont("Helvetica-Bold", 6)
        c.setFillColor(SYSTEM_GRAY)
        days = ["M", "T", "W", "T", "F", "S", "S"]
        for i, d in enumerate(days):
            c.drawCentredString(mini_x + i*(mini_w/7) + (mini_w/14), mini_y, d)
        
        # Calendar Days
        weeks = cal.monthdayscalendar(year, m)
        for r, week in enumerate(weeks):
            wy = mini_y - 4.5*mm - r*3.8*mm
            for d_idx, day in enumerate(week):
                if day != 0:
                    c.setFont("Helvetica", 7)
                    dt = datetime(year, m, day)
                    if dt.weekday() >= 5:
                        c.setFillColor(SYSTEM_GRAY)
                    else:
                        c.setFillColor(LABEL_COLOR)
                    
                    dx = mini_x + d_idx*(mini_w/7) + (mini_w/14)
                    c.drawCentredString(dx, wy, str(day))
                    # Link to Daily Page
                    c.linkRect("", f"Day_{year}_{m}_{day}", (dx - 2*mm, wy - 1*mm, dx + 2*mm, wy + 3*mm), Border='[0 0 0]')
    c.restoreState()

def draw_six_month_overview(c, year, start_month, W, H):
    margin = 20 * mm
    c.saveState()
    
    # Background
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Header
    c.setFont("Helvetica-Bold", 34)
    c.setFillColor(LABEL_COLOR)
    c.drawString(margin, H - 22*mm, f"{year}")
    c.setFont("Helvetica", 34)
    c.drawString(margin + c.stringWidth(f"{year} ", "Helvetica-Bold", 34), H - 22*mm, "Summary")
    
    # Side Tabs
    draw_side_tabs(c, W, H)
    
    # Navigation Tabs
    tab_w = 32 * mm
    gap = 3 * mm
    r_margin = 15 * mm
    draw_apple_tab(c, W - r_margin - tab_w*3 - gap*2, H - 22*mm, tab_w, 9*mm, "Calendar", destination="YearlySummary", icon_key="calendar")
    draw_apple_tab(c, W - r_margin - tab_w*2 - gap, H - 22*mm, tab_w, 9*mm, "Summary", active=True, destination="SixMonth_1", icon_key="overview")
    draw_apple_tab(c, W - r_margin - tab_w, H - 22*mm, tab_w, 9*mm, "Tracker", destination="YearlyTracker", icon_key="goals")
    
    # 6 Columns for 6 Months
    cols = 6
    col_w = (W - 2*margin) / cols
    top_y = H - 40*mm
    bottom_y = 15*mm
    row_h = (top_y - bottom_y - 10*mm) / 31
    
    for i in range(cols):
        m = start_month + i
        x = margin + i * col_w
        
        # Month Header (Grouped Style) - Clickable
        month_color = MONTH_COLORS[m-1]
        c.setFillColor(SYSTEM_GRAY_6)
        c.roundRect(x + 1*mm, top_y - 2*mm, col_w - 2*mm, 7*mm, 2*mm, fill=1, stroke=0)
        c.setFillColor(month_color)
        c.setFont("Helvetica-Bold", 9)
        month_name = calendar.month_name[m].upper()
        c.drawCentredString(x + col_w/2, top_y + 0.5*mm, month_name)
        c.linkRect("", f"Month_{m}", (x + 1*mm, top_y - 2*mm, x + col_w - 1*mm, top_y + 5*mm), Border='[0 0 0]')
        
        # Days
        for day in range(1, 32):
            y = top_y - 8*mm - (day-1) * row_h
            
            try:
                dt = datetime(year, m, day)
                is_weekend = dt.weekday() >= 5
                
                # Row Background
                if is_weekend:
                    c.setFillColor(colors.HexColor("#EBE8D8")) # Slightly darker for weekends
                else:
                    c.setFillColor(CARD_COLOR)
                c.rect(x + 1*mm, y - row_h/2, col_w - 2*mm, row_h, fill=1, stroke=0)
                
                # Separator
                c.setStrokeColor(SEPARATOR_COLOR)
                c.setLineWidth(0.05)
                c.line(x + 2*mm, y - row_h/2, x + col_w - 2*mm, y - row_h/2)
                
                # Day Number
                c.setFillColor(LABEL_COLOR if not is_weekend else SYSTEM_GRAY)
                c.setFont("Helvetica", 6.5)
                c.drawString(x + 2.5*mm, y - 1*mm, str(day))
                
                # Day Name (Initial)
                c.setFont("Helvetica", 5)
                c.setFillColor(SYSTEM_GRAY_2)
                c.drawString(x + 6*mm, y - 1*mm, dt.strftime("%a")[0])
                
                # Link to Daily Page
                c.linkRect("", f"Day_{year}_{m}_{day}", (x + 1*mm, y - row_h/2, x + col_w - 1*mm, y + row_h/2), Border='[0 0 0]')
                
            except ValueError:
                pass
    c.restoreState()

def draw_monthly_page(c, year, month, W, H):
    margin = 20 * mm
    month_color = MONTH_COLORS[month-1]
    c.saveState()
    
    # Background
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Header
    c.setFont("Helvetica-Bold", 34)
    c.setFillColor(month_color)
    c.drawString(margin, H - 22*mm, calendar.month_name[month])
    
    # Side Tabs
    draw_side_tabs(c, W, H, current_month=month)
    
    # Navigation Tabs
    tab_w = 32 * mm
    gap = 3 * mm
    r_margin = 15 * mm
    draw_apple_tab(c, W - r_margin - tab_w*3 - gap*2, H - 22*mm, tab_w, 9*mm, "Calendar", destination="YearlySummary", color=month_color, icon_key="calendar")
    draw_apple_tab(c, W - r_margin - tab_w*2 - gap, H - 22*mm, tab_w, 9*mm, "Summary", destination="SixMonth_1", color=month_color, icon_key="overview")
    draw_apple_tab(c, W - r_margin - tab_w, H - 22*mm, tab_w, 9*mm, "Tracker", destination="YearlyTracker", color=month_color, icon_key="goals")
    
    # Sidebar (Left) - 25% width
    sidebar_w = (W - 2*margin) * 0.25
    # Reduced line counts and spacing to fit on screen
    sections = [("Key Dates", 4, "important"), ("Monthly Tasks", 4, "goals"), ("Notes", 5, "notes")]
    sec_y = H - 45*mm
    line_h = 6.0 * mm
    
    for title, num_lines, icon_key in sections:
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(month_color)
        draw_icon(c, icon_key, margin + 2*mm, sec_y, 4*mm, month_color)
        c.drawString(margin + 8*mm, sec_y, title)
        sec_y -= 4.5*mm
        
        # Grouped List Background
        group_h = num_lines * line_h
        c.setFillColor(SYSTEM_GRAY_6)
        c.roundRect(margin, sec_y - group_h, sidebar_w, group_h, 4*mm, fill=1, stroke=0)
        
        c.setStrokeColor(SEPARATOR_COLOR)
        c.setLineWidth(0.1)
        for i in range(1, num_lines):
            ly = sec_y - i*line_h
            c.line(margin + 4*mm, ly, margin + sidebar_w - 4*mm, ly)
        
        sec_y -= group_h + 6*mm

    # Calendar Grid (Right)
    grid_x = margin + sidebar_w + 10*mm
    grid_w = W - margin - grid_x
    grid_top = H - 40*mm
    grid_bottom = 15*mm
    grid_h = grid_top - grid_bottom
    
    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(year, month)
    num_weeks = len(weeks)
    cell_w = grid_w / 7
    cell_h = grid_h / num_weeks
    
    # Day Headers
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(SYSTEM_GRAY)
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    for i, d in enumerate(days):
        c.drawCentredString(grid_x + i*cell_w + cell_w/2, grid_top + 3*mm, d)

    # Grid
    for r, week in enumerate(weeks):
        for d_idx, day in enumerate(week):
            x = grid_x + d_idx * cell_w
            y = grid_top - (r+1) * cell_h
            
            c.setStrokeColor(SEPARATOR_COLOR)
            c.setLineWidth(0.2)
            
            # Fill all cells with CARD_COLOR
            c.setFillColor(CARD_COLOR)
            c.rect(x, y, cell_w, cell_h, fill=1, stroke=1)
            
            if day != 0:
                dt = datetime(year, month, day)
                if dt.weekday() >= 5:
                    # Slightly darker for weekends
                    c.setFillColor(colors.HexColor("#EBE8D8"))
                    c.rect(x+0.2, y+0.2, cell_w-0.4, cell_h-0.4, fill=1, stroke=0)
                
                c.setFillColor(LABEL_COLOR)
                c.setFont("Helvetica-Bold", 12)
                c.drawString(x + 3*mm, y + cell_h - 7*mm, str(day))
                
                # Link to Daily Page (Entire Cell)
                c.linkRect("", f"Day_{year}_{month}_{day}", (x, y, x + cell_w, y + cell_h), Border='[0 0 0]')
    c.restoreState()

def draw_daily_page(c, date, W, H):
    margin = 20 * mm
    month_color = MONTH_COLORS[date.month-1]
    c.saveState()
    
    # Background
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Header (Native iPadOS Style)
    date_str = date.strftime("%A, %B %d").upper()
    year_str = date.strftime("%Y")
    
    # Date Badge
    badge_h = 10 * mm
    badge_y = H - 22 * mm
    badge_w = c.stringWidth(date_str + " " + year_str, "Helvetica-Bold", 12) + 10*mm
    
    c.saveState()
    c.setFillColor(SYSTEM_GRAY_6)
    c.roundRect(margin, badge_y, badge_w, badge_h, 3*mm, fill=1, stroke=0)
    c.restoreState()
    
    # Centering text vertically in badge
    text_y = badge_y + (badge_h / 2) - 1.8*mm
    c.setFillColor(month_color)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin + 5*mm, text_y, date_str)
    c.setFillColor(SECONDARY_LABEL)
    c.setFont("Helvetica", 12)
    c.drawString(margin + 5*mm + c.stringWidth(date_str + " ", "Helvetica-Bold", 12), text_y, year_str)
    
    # Side Tabs
    draw_side_tabs(c, W, H, current_month=date.month)
    
    # Navigation Tabs
    tab_w = 32 * mm
    gap = 3 * mm
    r_margin = 15 * mm
    draw_apple_tab(c, W - r_margin - tab_w*3 - gap*2, H - 22*mm, tab_w, 9*mm, "Calendar", destination="YearlySummary", color=month_color, icon_key="calendar")
    draw_apple_tab(c, W - r_margin - tab_w*2 - gap, H - 22*mm, tab_w, 9*mm, "Summary", destination="SixMonth_1", color=month_color, icon_key="overview")
    draw_apple_tab(c, W - r_margin - tab_w, H - 22*mm, tab_w, 9*mm, "Tracker", destination="YearlyTracker", color=month_color, icon_key="goals")
    
    # Layout: 3 Columns
    col_gap = 10 * mm
    col1_w = (W - 2*margin - 2*col_gap) * 0.30 # To Do
    col2_w = (W - 2*margin - 2*col_gap) * 0.30 # Priorities/Notes
    col3_w = (W - 2*margin - 2*col_gap) * 0.40 # Schedule
    
    top_y = H - 40*mm
    bottom_y = 15*mm
    available_h = top_y - bottom_y
    
    # Column 1: TO DO (Grouped List)
    x1 = margin
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(month_color)
    draw_icon(c, "todo", x1 + 2*mm, top_y + 5*mm, 4.5*mm, month_color)
    c.drawString(x1 + 8*mm, top_y + 5*mm, "To Do")
    
    num_todo = 14
    todo_h = available_h
    c.setFillColor(SYSTEM_GRAY_6)
    c.roundRect(x1, bottom_y, col1_w, todo_h, 5*mm, fill=1, stroke=0)
    
    # Add padding inside the box
    padding_top = 4*mm
    padding_bottom = 4*mm
    usable_todo_h = todo_h - padding_top - padding_bottom
    line_h = usable_todo_h / num_todo
    
    for i in range(num_todo):
        ly = (top_y - padding_top) - i*line_h
        if i > 0:
            c.setStrokeColor(SEPARATOR_COLOR)
            c.setLineWidth(0.1)
            c.line(x1 + 12*mm, ly, x1 + col1_w - 4*mm, ly)
        
        # Checkbox (Reminders Style)
        c.setStrokeColor(month_color)
        c.setStrokeAlpha(0.4)
        c.setLineWidth(0.6)
        c.circle(x1 + 6*mm, ly - line_h/2, 2.2*mm, stroke=1, fill=0)
        c.setStrokeAlpha(1.0)

    # Column 2: PRIORITIES & NOTES
    x2 = x1 + col1_w + col_gap
    
    # Priorities (Grouped List)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(month_color)
    draw_icon(c, "priorities", x2 + 2*mm, top_y + 5*mm, 4.5*mm, month_color)
    c.drawString(x2 + 8*mm, top_y + 5*mm, "Priorities")
    
    prio_h = 40 * mm
    c.setFillColor(SYSTEM_GRAY_6)
    c.roundRect(x2, top_y - prio_h, col2_w, prio_h, 5*mm, fill=1, stroke=0)
    
    prio_padding = 4*mm
    prio_line_h = (prio_h - 2*prio_padding) / 3
    for i in range(1, 3):
        ly = (top_y - prio_padding) - i*prio_line_h
        c.setStrokeColor(SEPARATOR_COLOR)
        c.setLineWidth(0.1)
        c.line(x2 + 4*mm, ly, x2 + col2_w - 4*mm, ly)
    
    # Notes (Rounded Box)
    notes_top = top_y - prio_h - 12*mm
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(month_color)
    draw_icon(c, "notes", x2 + 2*mm, notes_top + 5*mm, 4.5*mm, month_color)
    c.drawString(x2 + 8*mm, notes_top + 5*mm, "Notes")
    
    c.setFillColor(CARD_COLOR)
    c.roundRect(x2, bottom_y, col2_w, notes_top - bottom_y, 5*mm, fill=1, stroke=0)

    # Column 3: SCHEDULE (Clean Timeline)
    x3 = x2 + col2_w + col_gap
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(month_color)
    draw_icon(c, "schedule", x3 + 2*mm, top_y + 5*mm, 4.5*mm, month_color)
    c.drawString(x3 + 8*mm, top_y + 5*mm, "Schedule")
    
    num_hours = 16 # 06:00 to 21:00
    sched_h = available_h
    row_h = sched_h / num_hours
    
    for i in range(num_hours + 1):
        ly = top_y - i*row_h
        
        # Time Label - Centered vertically on the line
        if i < num_hours:
            time_str = f"{6+i:02d}:00"
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(SYSTEM_GRAY)
            c.drawRightString(x3 + 10*mm, ly - row_h/2 + 1*mm, time_str)
        
        # Horizontal Line
        c.setStrokeColor(SEPARATOR_COLOR)
        c.setLineWidth(0.1)
        c.line(x3 + 12*mm, ly, x3 + col3_w, ly)
        
    # Vertical Timeline Line
    c.setStrokeColor(month_color)
    c.setStrokeAlpha(0.4)
    c.setLineWidth(0.5)
    c.line(x3 + 12*mm, top_y, x3 + 12*mm, bottom_y)
    c.setStrokeAlpha(1.0)

    # Year Progress Bar (Centered at Bottom)
    day_of_year = date.timetuple().tm_yday
    total_days = 365
    progress = day_of_year / total_days
    
    bar_w = 80 * mm
    bar_h = 1.2 * mm
    text_space = 12 * mm
    total_w = bar_w + text_space
    
    bar_x = (W - total_w) / 2
    bar_y = 6 * mm
    
    c.saveState()
    # Background Bar
    c.setFillColor(SYSTEM_GRAY_4)
    c.roundRect(bar_x, bar_y, bar_w, bar_h, 0.6*mm, fill=1, stroke=0)
    
    # Progress Fill
    c.setFillColor(month_color)
    c.roundRect(bar_x, bar_y, bar_w * progress, bar_h, 0.6*mm, fill=1, stroke=0)
    
    # Percentage Text
    c.setFillColor(SECONDARY_LABEL)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(bar_x + bar_w + 2*mm, bar_y - 0.5*mm, f"{int(progress * 100)}%")
    c.restoreState()

    c.restoreState()

def generate_year_pdf(year, out_path):
    W, H = IPAD_PRO_11_LANDSCAPE
    c = canvas.Canvas(out_path, pagesize=(W, H))
    
    # 1. Cover
    c.bookmarkPage("Cover")
    draw_cover(c, W, H, f"{year}")
    c.showPage()
    
    # 2. Yearly Summary
    c.bookmarkPage("YearlySummary")
    draw_summary_page(c, year, W, H)
    c.showPage()
    
    # 2.5 Yearly Tracker
    c.bookmarkPage("YearlyTracker")
    draw_yearly_tracker(c, year, W, H)
    c.showPage()
    
    # 3. Six-Month Overviews
    c.bookmarkPage("SixMonth_1")
    draw_six_month_overview(c, year, 1, W, H)
    c.showPage()
    c.bookmarkPage("SixMonth_7")
    draw_six_month_overview(c, year, 7, W, H)
    c.showPage()
    
    # 4. Monthly & Daily Pages
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    
    current_month = 0
    curr = start_date
    while curr <= end_date:
        if curr.month != current_month:
            current_month = curr.month
            c.bookmarkPage(f"Month_{current_month}")
            draw_monthly_page(c, year, current_month, W, H)
            c.showPage()
        
        c.bookmarkPage(f"Day_{year}_{curr.month}_{curr.day}")
        draw_daily_page(c, curr, W, H)
        c.showPage()
        curr += timedelta(days=1)
        
    c.save()

if __name__ == "__main__":
    # Default to next year if run directly
    target_year = datetime.now().year + 1
    generate_year_pdf(target_year, f"planner_{target_year}.pdf")
