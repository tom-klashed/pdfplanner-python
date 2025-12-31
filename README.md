# Planner PDF Generator

This is completely vibe coded using VS Code with Github Copilot and Gemini 3 Flash.

If you just want the planner it's the PDF file above named planner_2026.pdf.

I've also added two sample PDFs for meeting notes and BI requirements. These were created in the same way.

## Usage

To generate the default 2026 planner:
```bash
python generate_planner.py
```

To generate a planner for a specific year:
```bash
python generate_planner.py 2027
```

The output will be saved as `planner_{year}.pdf`.

## Requirements
- reportlab
- svglib
- Pillow
- lxml (for svglib)