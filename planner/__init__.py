"""Simple planner package"""
from .templates.planner import generate_year_pdf
from .templates.meeting_notes import generate_meeting_notes_pdf
from .templates.bi_requirements import generate_bi_requirements_pdf

__all__ = ["generate_year_pdf", "generate_meeting_notes_pdf", "generate_bi_requirements_pdf"]

