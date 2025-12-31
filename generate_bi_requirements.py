import sys
import os
from planner.bi_requirements_generator import generate_bi_requirements_pdf

def main():
    output_file = "bi_requirements.pdf"
    
    print(f"Generating BI Requirements PDF...")
    generate_bi_requirements_pdf(output_file)
    print(f"Successfully generated {output_file}")

if __name__ == "__main__":
    main()
