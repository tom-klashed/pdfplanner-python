import sys
from planner import generate_meeting_notes_pdf

def main():
    filename = "meeting_notes.pdf"
    print(f"Generating {filename}...")
    generate_meeting_notes_pdf(filename)
    print("Done!")

if __name__ == "__main__":
    main()
