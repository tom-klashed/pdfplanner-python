import sys
from datetime import datetime
from planner import generate_year_pdf


def main():
    # Default to 2026 as requested, or take from command line
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
        except ValueError:
            print("Usage: python generate_planner.py [year]")
            sys.exit(1)
    else:
        year = 2026
        
    filename = f"planner_{year}.pdf"
    print(f"Generating {filename}...")
    generate_year_pdf(year, filename)
    print("Done!")


if __name__ == "__main__":
    main()
