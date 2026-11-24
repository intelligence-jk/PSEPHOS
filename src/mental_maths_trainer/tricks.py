"""Question generators. Each question carries its answer and a step by step explanation.

Every explanation line that states arithmetic is written as `a + b = c`, `a x b = c`,
`a - b = c` or `a / b = c`, so the tests can re-check each one.
"""
import random
from dataclasses import dataclass, field

TOPICS = ("times11", "squares5", "near100", "divisibility", "percentages")


@dataclass
class Question:
    topic: str
    prompt: str
    answer: object          # int, or "yes" / "no" for divisibility
    steps: list = field(default_factory=list)


def _times11(rng):
    n = rng.choice([rng.randint(12, 99), rng.randint(100, 999)])
    digits = [int(c) for c in str(n)]
    pairs = [digits[i] + digits[i + 1] for i in range(len(digits) - 1)]
    pieces = [digits[0]] + pairs + [digits[-1]]
    steps = [f"Write the digits of {n} with a gap: {' '.join(map(str, digits))}.",
             f"Keep the first digit {digits[0]} at the front and the last digit {digits[-1]} at the back."]
    for i in range(len(digits) - 1):
        steps.append(f"Add each neighbouring pair: {digits[i]} + {digits[i + 1]} = {pairs[i]}.")
    steps.append("In order, the pieces are: " + ", ".join(map(str, pieces)) + ".")
    carry, out = 0, []
    for piece in reversed(pieces):
        val = piece + carry
        if carry:
            steps.append(f"Carry {carry} into {piece}: {piece} + {carry} = {val}.")
        out.append(val % 10)
        carry = val // 10
    if carry:
        out.append(carry)
    answer = int("".join(map(str, reversed(out))))
    steps.append(f"Read the digits off: {n} x 11 = {answer}.")
    return Question("times11", f"{n} x 11 = ?", answer, steps)


def _squares5(rng):
    a = rng.randint(1, 19)
    n = 10 * a + 5
    prod = a * (a + 1)
    answer = prod * 100 + 25
    steps = [f"{n} ends in 5, so take the digits in front of the 5: {a}.",
             f"Multiply it by the next whole number: {a} x {a + 1} = {prod}.",
             f"Write 25 after that: {prod} x 100 + 25 = {answer}.",
             f"Why it works: (10a + 5) squared = 100 x a x (a + 1) + 25.",
             f"So {n} squared is {answer}."]
    return Question("squares5", f"{n} squared = ?", answer, steps)


def _near100(rng):
    a, b = rng.randint(80, 99), rng.randint(80, 99)
    x, y = 100 - a, 100 - b
    left = a - y
    prod = x * y
    answer = left * 100 + prod
    steps = [f"Both numbers are just below 100. Find the gaps: 100 - {a} = {x} and 100 - {b} = {y}.",
             f"Cross subtract, one number minus the other's gap: {a} - {y} = {left}.",
             f"(Check with the other cross: {b} - {x} = {b - x}. It is the same.)",
             f"Multiply the gaps: {x} x {y} = {prod}.",
             f"Put them together as hundreds and the rest: {left} x 100 + {prod} = {answer}.",
             f"So {a} x {b} = {answer}."]
    return Question("near100", f"{a} x {b} = ?", answer, steps)


def _digit_sum_steps(n):
    ds = [int(c) for c in str(n)]
    return ds, " + ".join(map(str, ds)), sum(ds)


def _divisibility(rng):
    d = rng.choice([2, 3, 4, 5, 6, 8, 9, 10, 11])
    n = rng.randint(100, 99999)
    if rng.random() < 0.5:                 # make about half of them divisible
        n = max(d, (n // d) * d)
    yes = n % d == 0
    word = "divisible" if yes else "not divisible"
    steps = []
    if d in (3, 9):
        _, expr, s = _digit_sum_steps(n)
        steps.append(f"Add the digits: {expr} = {s}.")
        steps.append(f"Is {s} in the {d} times table? {'Yes' if s % d == 0 else 'No'}.")
    elif d == 6:
        _, expr, s = _digit_sum_steps(n)
        steps.append(f"6 needs both 2 and 3. The last digit is {n % 10}, so {'even' if n % 2 == 0 else 'odd'}.")
        steps.append(f"Add the digits: {expr} = {s}. {'In' if s % 3 == 0 else 'Not in'} the 3 times table.")
    elif d in (4, 8):
        k = 2 if d == 4 else 3
        tail = n % (10 ** k)
        steps.append(f"Look only at the last {k} digits: {tail}.")
        q, r = divmod(tail, d)
        if r == 0:
            steps.append(f"{q} x {d} = {tail}, so it divides exactly.")
        else:
            steps.append(f"{q} x {d} + {r} = {tail}, so there is a remainder of {r}.")
    elif d in (2, 5, 10):
        L = n % 10
        q, r = divmod(L, d)
        rule = {2: "It must be even (0, 2, 4, 6, 8).", 5: "It must be 0 or 5.", 10: "It must be 0."}[d]
        steps.append(f"Look only at the last digit: {L}. {rule}")
        steps.append(f"Check it against {d}: {q} x {d} + {r} = {L}, remainder {r}.")
    else:  # 11: alternating sum
        ds = [int(c) for c in str(n)]
        odd, even = ds[0::2], ds[1::2]
        so, se = sum(odd), sum(even)
        steps.append("Add the digits in places 1, 3, 5 (from the left): " + " + ".join(map(str, odd)) + f" = {so}.")
        if even:
            steps.append("Add the digits in places 2, 4, 6: " + " + ".join(map(str, even)) + f" = {se}.")
        hi, lo = max(so, se), min(so, se)
        steps.append(f"Take the difference: {hi} - {lo} = {hi - lo}.")
        steps.append("Divisible by 11 only if the difference is 0 or in the 11 times table. "
                     f"Here that is {'true' if yes else 'not true'}.")
    steps.append(f"So {n} is {word} by {d}.")
    return Question("divisibility", f"Is {n} divisible by {d}? (yes/no)", "yes" if yes else "no", steps)


def _percentages(rng):
    p = rng.choice([5, 10, 15, 20, 25, 30, 40, 50, 75])
    n = 20 * rng.randint(2, 50)
    t = n // 10
    steps = []
    if p == 10:
        ans = t
        steps.append(f"10% is one tenth: {n} / 10 = {ans}.")
    elif p in (20, 30, 40):
        k = p // 10
        ans = t * k
        steps += [f"Find 10% first: {n} / 10 = {t}.", f"{p}% is {k} tens: {t} x {k} = {ans}."]
    elif p == 5:
        ans = t // 2
        steps += [f"Find 10% first: {n} / 10 = {t}.", f"5% is half of that: {t} / 2 = {ans}."]
    elif p == 15:
        h = t // 2
        ans = t + h
        steps += [f"Find 10% first: {n} / 10 = {t}.", f"5% is half of that: {t} / 2 = {h}.",
                  f"15% is 10% plus 5%: {t} + {h} = {ans}."]
    elif p == 25:
        ans = n // 4
        steps.append(f"25% is a quarter: {n} / 4 = {ans}.")
    elif p == 50:
        ans = n // 2
        steps.append(f"50% is a half: {n} / 2 = {ans}.")
    else:  # 75
        q = n // 4
        ans = q * 3
        steps += [f"75% is three quarters. One quarter: {n} / 4 = {q}.", f"Three of them: {q} x 3 = {ans}."]
    steps.append(f"So {p}% of {n} is {ans}.")
    return Question("percentages", f"{p}% of {n} = ?", ans, steps)


_MAKERS = {"times11": _times11, "squares5": _squares5, "near100": _near100,
           "divisibility": _divisibility, "percentages": _percentages}


def make_question(topic, rng):
    return _MAKERS[topic](rng)


def generate_questions(topic="all", n=10, seed=None):
    """n questions. The same seed always gives the same sequence. topic 'all' mixes every topic."""
    if topic != "all" and topic not in _MAKERS:
        raise ValueError(f"unknown topic {topic!r}; choose from {', '.join(TOPICS)} or all")
    rng = random.Random(seed)
    return [make_question(topic if topic != "all" else rng.choice(TOPICS), rng) for _ in range(n)]
