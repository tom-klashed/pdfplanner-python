from reportlab.lib import colors
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.lib.units import mm
import os
from .constants import ICONS, ICON_DIR, CARD_COLOR, SEPARATOR_COLOR, LABEL_COLOR

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
