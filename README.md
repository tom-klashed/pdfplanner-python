# Planner PDF Generator

This is completed vibe coded, so please excuse.

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