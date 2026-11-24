"""Terminal session. The score lives in memory only; nothing is written to disk."""
import time


class Session:
    def __init__(self):
        self.asked = 0
        self.correct = 0
        self.streak = 0
        self.best_streak = 0

    def record(self, ok):
        self.asked += 1
        if ok:
            self.correct += 1
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
        else:
            self.streak = 0

    def summary(self):
        return f"Score: {self.correct}/{self.asked}. Best streak: {self.best_streak}."


def normalise(text, expected):
    t = text.strip().lower()
    if expected in ("yes", "no"):
        return {"y": "yes", "yes": "yes", "n": "no", "no": "no"}.get(t)
    try:
        return int(t.replace(",", ""))
    except ValueError:
        return None


def run_session(questions, input_fn=input, print_fn=print, timed=None, clock=time.monotonic):
    """Ask the questions. timed = total seconds (checked after each answer), or None.

    Type q to quit. Returns the Session.
    """
    s = Session()
    start = clock()
    for i, q in enumerate(questions, 1):
        if timed is not None and clock() - start >= timed:
            print_fn("Time is up.")
            break
        left = "" if timed is None else f" [{max(0, int(timed - (clock() - start)))}s left]"
        raw = input_fn(f"Q{i}{left}: {q.prompt} ")
        if raw.strip().lower() == "q":
            break
        ok = normalise(raw, q.answer) == q.answer
        s.record(ok)
        print_fn("Correct!" if ok else f"Not quite. The answer is {q.answer}.")
        for line in q.steps:
            print_fn("  " + line)
        if timed is not None and clock() - start >= timed:
            print_fn("Time is up.")
            break
    print_fn(s.summary())
    return s
