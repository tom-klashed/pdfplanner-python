# Planner PDF Generator

This is completely vibe coded using VS Code with Github Copilot and Gemini 3 Flash.

If you just want the planner it's the PDF file above named planner_2026.pdf.

I've also added two sample PDFs for meeting notes and BI requirements. These were created in the same way.

## Usage

The project now uses a single entry point `generate.py` to create different PDF templates.

### Generate Yearly Planner
To generate the default 2026 planner:
```bash
python generate.py planner
```

To generate a planner for a specific year:
```bash
python generate.py planner --year 2027
```

### Generate Meeting Notes
```bash
python generate.py meeting
```

### Generate BI Requirements
```bash
python generate.py bi_requirements
```

The output will be saved as a PDF in the current directory.

## Requirements
- reportlab
- svglib
- Pillow
- lxml (for svglib)