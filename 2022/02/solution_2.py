from enum import Enum
from typing import List


class Hand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):
    DRAW = 0
    WIN = 1
    LOSS = 2


HAND_MAP = {
    "A": Hand.ROCK,
    "B": Hand.PAPER,
    "C": Hand.SCISSORS,
}

OUTCOME_MAP = {
    "X": Outcome.LOSS,
    "Y": Outcome.DRAW,
    "Z": Outcome.WIN,
}

HAND_POINTS = {Hand.ROCK: 1, Hand.PAPER: 2, Hand.SCISSORS: 3}
OUTCOME_POINTS = {Outcome.WIN: 6, Outcome.DRAW: 3, Outcome.LOSS: 0}


def get_hand_score(hand: Hand) -> int:
    return HAND_POINTS[hand]


def get_outcome_score(outcome: Outcome) -> int:
    return OUTCOME_POINTS[outcome]


def calc_outcome(my_hand: Hand, opponent_hand: Hand) -> Outcome:
    mod_difference = (my_hand.value - opponent_hand.value + 3) % 3
    if mod_difference == 0:
        return Outcome.DRAW
    elif mod_difference == 1:
        return Outcome.WIN
    else:
        return Outcome.LOSS


def choose_hand(outcome: Outcome, opponent_hand: Hand) -> Hand:
    for potential_hand in Hand:
        potential_outcome = calc_outcome(potential_hand, opponent_hand)
        if potential_outcome == outcome:
            return potential_hand
    raise Exception("couldn't find a proper hand")


def read_input() -> List[str]:
    with open("input.txt") as f:
        lines = f.readlines()
    return lines


def process_input(lines: List[str]) -> List[List[str]]:
    tuples = []
    for line in lines:
        tuples.append(line.split())
    return tuples


def calculate_overall_score(rounds: List[List[str]]) -> int:
    score = 0
    for elf, outcome_raw in rounds:
        elf_hand = HAND_MAP[elf]
        outcome = OUTCOME_MAP[outcome_raw]
        my_hand = choose_hand(outcome=outcome, opponent_hand=elf_hand)
        score += get_hand_score(my_hand)
        score += get_outcome_score(outcome)
    return score


def main():
    input_lines = read_input()
    rounds = process_input(input_lines)
    overall_score = calculate_overall_score(rounds)
    print(f"my overall score is {overall_score}")


if __name__ == "__main__":
    main()
