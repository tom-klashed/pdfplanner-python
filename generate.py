import argparse
from datetime import datetime
from planner import (
    generate_year_pdf, 
    generate_meeting_notes_pdf, 
    generate_bi_requirements_pdf
)

def main():
    parser = argparse.ArgumentParser(description="Generate PDF Planner templates.")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Planner command
    planner_parser = subparsers.add_parser("planner", help="Generate a yearly planner")
    planner_parser.add_argument("--year", type=int, default=datetime.now().year + 1, help="Year for the planner")
    planner_parser.add_argument("--output", type=str, help="Output file path")

    # Meeting Notes command
    meeting_parser = subparsers.add_parser("meeting_notes", help="Generate meeting notes template")
    meeting_parser.add_argument("--output", type=str, default="meeting_notes.pdf", help="Output file path")

    # BI Requirements command
    bi_parser = subparsers.add_parser("bi_requirements", help="Generate BI requirements template")
    bi_parser.add_argument("--output", type=str, default="bi_requirements.pdf", help="Output file path")

    args = parser.parse_args()

    if args.command == "planner":
        year = args.year
        output = args.output or f"planner_{year}.pdf"
        print(f"Generating planner for {year} to {output}...")
        generate_year_pdf(year, output)
        print("Done!")
    
    elif args.command == "meeting_notes":
        print(f"Generating meeting notes to {args.output}...")
        generate_meeting_notes_pdf(args.output)
        print("Done!")
    
    elif args.command == "bi_requirements":
        print(f"Generating BI requirements to {args.output}...")
        generate_bi_requirements_pdf(args.output)
        print("Done!")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
