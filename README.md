# PSEPHOS: Greek for the pebble used for counting

Formerly `mental-maths-trainer`.

Mental maths trainer with the tricks explained.

## What it does
Speed in mental maths comes from knowing why a trick works, not from memorising answers. This terminal trainer asks seeded questions on five tricks (multiply by 11, squares of numbers ending in 5, near-100 multiplication, divisibility rules, percentages). After every answer, right or wrong, it shows the trick step by step. The score is kept in memory for the session only; nothing about you is saved. There is a timed mode, and `--seed` gives the same questions every time.

## Example
```bash
printf '8526\n8000\n' | python -m mental_maths_trainer --seed 3 -n 2 --topic near100
```
Real output (typed answers are not echoed when piped):
```
Type your answer and press Enter. Type q to quit.
Q1: 87 x 98 = ? Correct!
  Both numbers are just below 100. Find the gaps: 100 - 87 = 13 and 100 - 98 = 2.
  Cross subtract, one number minus the other's gap: 87 - 2 = 85.
  (Check with the other cross: 98 - 13 = 85. It is the same.)
  Multiply the gaps: 13 x 2 = 26.
  Put them together as hundreds and the rest: 85 x 100 + 26 = 8526.
  So 87 x 98 = 8526.
Q2: 97 x 84 = ? Not quite. The answer is 8148.
  Both numbers are just below 100. Find the gaps: 100 - 97 = 3 and 100 - 84 = 16.
  Cross subtract, one number minus the other's gap: 97 - 16 = 81.
  (Check with the other cross: 84 - 3 = 81. It is the same.)
  Multiply the gaps: 3 x 16 = 48.
  Put them together as hundreds and the rest: 81 x 100 + 48 = 8148.
  So 97 x 84 = 8148.
Score: 1/2. Best streak: 1.
```
Options: `--topic` (times11, squares5, near100, divisibility, percentages, all), `-n` number of questions, `--seed`, `--timed SECONDS` (checked after each answer), `--list` (show every question with its answer and steps instead of quizzing). Type `q` to quit. Divisibility answers are yes or no.

## The maths behind it
- **Times 11:** n x 11 = n x 10 + n. Writing n shifted one place and adding it to itself means each digit gets added to its neighbour, so 347 x 11 gives the pieces 3, 3+4, 4+7, 7 and then you carry.
- **Squares ending in 5:** write the number as 10a + 5. Then (10a + 5)^2 = 100a^2 + 100a + 25 = 100 x a(a + 1) + 25. So multiply a by the next number and put 25 after it.
- **Near 100:** let the numbers be 100 - x and 100 - y. Then (100 - x)(100 - y) = 10000 - 100x - 100y + xy = 100 x (100 - x - y) + xy. And 100 - x - y is the same as (100 - x) - y, the cross subtraction.
- **Divisibility:** 10 leaves remainder 1 when divided by 3 or 9, so every place value does too, and a number has the same remainder as its digit sum. 100 is a multiple of 4 and 1000 of 8, so only the last two or three digits matter. 10 is one less than 11, so 10^k leaves remainder 1 or -1 in turn, which gives the alternating digit sum for 11.
- **Percentages:** p% of n is p x n / 100. Building p from 10%, 5%, 25% and 50% keeps every step to a halving, a tenth or a quarter.

## Install and run
```bash
python -m pip install -e .
python -m pytest
python -m mental_maths_trainer --topic times11 -n 5
```
Python 3.10 or newer, standard library only.

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
