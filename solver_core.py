from itertools import product

def score(secret, guess):
    strike = sum(s == g for s, g in zip(secret, guess))

    common = sum(
        min(secret.count(d), guess.count(d))
        for d in set(guess)
    )
    ball = common - strike
    miss = 4 - strike - ball
    return strike, ball, miss


class Solver:
    def __init__(self):
        self.candidates = list(product(range(1, 5), repeat=4))

    def apply_hint(self, guess, hint):
        s, b, m = hint
        self.candidates = [
            c for c in self.candidates
            if score(list(c), guess) == (s, b, m)
        ]

    def next_guess(self):
        return list(self.candidates[0]) if self.candidates else None
