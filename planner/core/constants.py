from reportlab.lib import colors
import os

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
CARD_COLOR = colors.HexColor("#F2F0E7")

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
# Note: We use a relative path from the core directory to the assets directory
ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "icons")
ICONS = {
    "todo": "add_task_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "priorities": "bookmark_star_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "notes": "event_list_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "schedule": "schedule_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "home": "today_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "important": "notification_important_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "goals": "bookmark_check_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "calendar": "calendar_month_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "overview": "date_range_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg",
    "discovery": "list_alt_check_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg"
}
