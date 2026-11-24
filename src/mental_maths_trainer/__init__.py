"""Mental maths trainer with the tricks explained."""
from .tricks import TOPICS, Question, generate_questions, make_question
from .session import Session, run_session

__all__ = ["TOPICS", "Question", "generate_questions", "make_question", "Session", "run_session"]
