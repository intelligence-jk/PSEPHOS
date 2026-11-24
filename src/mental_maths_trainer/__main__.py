import argparse
import sys

from .session import run_session
from .tricks import TOPICS, generate_questions


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m mental_maths_trainer",
                                 description="Mental maths trainer with the tricks explained")
    ap.add_argument("--topic", default="all", choices=("all",) + TOPICS)
    ap.add_argument("-n", type=int, default=10, help="number of questions (default 10)")
    ap.add_argument("--seed", type=int, default=None, help="same seed, same questions")
    ap.add_argument("--timed", type=int, metavar="SECONDS", default=None,
                    help="stop after this many seconds (checked after each answer)")
    ap.add_argument("--list", action="store_true", help="print the questions with answers and tricks, no quiz")
    a = ap.parse_args(argv)
    qs = generate_questions(a.topic, a.n, a.seed)
    if a.list:
        for i, q in enumerate(qs, 1):
            print(f"Q{i}: {q.prompt} -> {q.answer}")
            for line in q.steps:
                print("  " + line)
        return 0
    print("Type your answer and press Enter. Type q to quit.")
    try:
        run_session(qs, timed=a.timed)
    except (EOFError, KeyboardInterrupt):
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
