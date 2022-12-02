from enum import Enum
from typing import List


class Hand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


HAND_MAP = {
    "A": Hand.ROCK,
    "X": Hand.ROCK,
    "B": Hand.PAPER,
    "Y": Hand.PAPER,
    "C": Hand.SCISSORS,
    "Z": Hand.SCISSORS,
}

HAND_POINTS = {Hand.ROCK: 1, Hand.PAPER: 2, Hand.SCISSORS: 3}


def calc_hand_score(hand: Hand) -> int:
    return HAND_POINTS[hand]


def calc_outcome_score(my_hand: Hand, opponent_hand: Hand) -> int:
    mod_difference = (my_hand.value - opponent_hand.value + 3) % 3
    if mod_difference == 0:
        return 3
    elif mod_difference == 1:
        return 6
    else:
        return 0


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
    for elf, me in rounds:
        elf_hand = HAND_MAP[elf]
        my_hand = HAND_MAP[me]
        score += calc_hand_score(my_hand)
        score += calc_outcome_score(my_hand=my_hand, opponent_hand=elf_hand)
    return score


def main():
    input_lines = read_input()
    rounds = process_input(input_lines)
    overall_score = calculate_overall_score(rounds)
    print(f"my overall score is {overall_score}")


if __name__ == "__main__":
    main()
