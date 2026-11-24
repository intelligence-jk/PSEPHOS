import re
from fractions import Fraction

import pytest
from mental_maths_trainer import generate_questions, TOPICS, run_session, Session
from mental_maths_trainer.__main__ import main

EQ = re.compile(r"\d+(?: [+x/-] \d+)+ = \d+")


def check_equations(text):
    found = EQ.findall(text)
    for eq in found:
        lhs, rhs = eq.split(" = ")
        expr = re.sub(r"\d+", lambda m: f"Fraction({m.group()})", lhs.replace(" x ", " * "))
        assert eval(expr) == Fraction(int(rhs)), f"wrong arithmetic in: {eq}"
    return found


def independent(q):
    """Recompute the answer from the prompt alone."""
    nums = [int(x) for x in re.findall(r"\d+", q.prompt)]
    if q.topic == "times11":
        return nums[0] * 11
    if q.topic == "squares5":
        return nums[0] ** 2
    if q.topic == "near100":
        return nums[0] * nums[1]
    if q.topic == "divisibility":
        return "yes" if nums[0] % nums[1] == 0 else "no"
    p, n = nums
    return Fraction(p * n, 100)


@pytest.mark.parametrize("topic", TOPICS)
def test_every_answer_is_right(topic):
    for seed in range(40):
        for q in generate_questions(topic, 25, seed):
            assert independent(q) == q.answer, q.prompt


@pytest.mark.parametrize("topic", TOPICS)
def test_every_explanation_matches_arithmetic(topic):
    for seed in range(40):
        for q in generate_questions(topic, 25, seed):
            text = "\n".join(q.steps)
            assert check_equations(text), f"no checkable arithmetic: {q.prompt}"
            # the last line states the answer
            ans = "not divisible" if q.answer == "no" else "divisible" if q.answer == "yes" else str(q.answer)
            assert ans in q.steps[-1], (q.prompt, q.steps[-1])


def test_divisibility_has_both_answers():
    answers = {q.answer for q in generate_questions("divisibility", 200, 1)}
    assert answers == {"yes", "no"}


def test_every_divisor_and_percentage_appear():
    ds = {int(re.findall(r"\d+", q.prompt)[1]) for q in generate_questions("divisibility", 500, 2)}
    assert ds == {2, 3, 4, 5, 6, 8, 9, 10, 11}
    ps = {int(re.findall(r"\d+", q.prompt)[0]) for q in generate_questions("percentages", 500, 2)}
    assert ps == {5, 10, 15, 20, 25, 30, 40, 50, 75}


def test_seed_gives_fixed_sequence():
    a = generate_questions("all", 12, 7)
    b = generate_questions("all", 12, 7)
    assert [q.prompt for q in a] == [q.prompt for q in b]
    assert [q.prompt for q in a] != [q.prompt for q in generate_questions("all", 12, 8)]
    assert [q.prompt for q in generate_questions("times11", 3, 0)] == \
           [q.prompt for q in generate_questions("times11", 3, 0)]


def test_known_examples():
    qs = generate_questions("near100", 200, 3)
    q = next(q for q in qs if q.prompt == "96 x 93 = ?") if any(q.prompt == "96 x 93 = ?" for q in qs) else None
    if q:
        assert q.answer == 8928
    assert generate_questions("squares5", 1, 0)[0].answer % 100 == 25


def test_unknown_topic():
    with pytest.raises(ValueError):
        generate_questions("algebra", 1, 0)


def test_session_scores_in_memory():
    qs = generate_questions("squares5", 3, 5)
    answers = iter([str(qs[0].answer), "0", "q"])
    out = []
    s = run_session(qs, input_fn=lambda _: next(answers), print_fn=out.append)
    assert (s.correct, s.asked, s.best_streak) == (1, 2, 1)
    assert any("Correct!" in x for x in out) and any("Not quite" in x for x in out)
    assert out[-1] == "Score: 1/2. Best streak: 1."


def test_timed_mode_stops():
    qs = generate_questions("percentages", 10, 1)
    t = iter(range(0, 1000, 20))           # each clock() call advances 20 s
    out = []
    s = run_session(qs, input_fn=lambda _: "1", print_fn=out.append, timed=45, clock=lambda: next(t))
    assert s.asked < 10
    assert "Time is up." in out


def test_yes_no_answers_accepted():
    q = generate_questions("divisibility", 1, 4)[0]
    reply = "y" if q.answer == "yes" else "no"
    s = run_session([q], input_fn=lambda _: reply, print_fn=lambda _: None)
    assert s.correct == 1


def test_cli_list(capsys):
    assert main(["--topic", "times11", "-n", "2", "--seed", "1", "--list"]) == 0
    out = capsys.readouterr().out
    assert "x 11" in out and "Q2" in out
