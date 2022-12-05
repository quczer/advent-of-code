from copy import deepcopy
from dataclasses import dataclass
from typing import List, Literal, Optional, Tuple


@dataclass
class Instruction:
    quantity: int
    move_from: int
    move_to: int


class Board:
    def __init__(self, size: int):
        self.size = size
        self.stacks: List[List[str]] = [[] for _ in range(size)]

    def __repr__(self) -> str:
        return f"Board({self.size})\ncontent: {self.stacks}"

    def put(self, crate: str, position: int) -> None:
        self.stacks[position - 1].append(crate)

    def pop(self, position: int) -> str:
        crate = self.stacks[position - 1].pop()
        return crate

    def apply_9000(self, instruction: Instruction) -> None:
        for _ in range(instruction.quantity):
            crate = self.pop(instruction.move_from)
            self.put(crate, instruction.move_to)

    def apply_9001(self, instruction: Instruction) -> None:
        crates = []
        for _ in range(instruction.quantity):
            crates.append(self.pop(instruction.move_from))
        for crate in reversed(crates):
            self.put(crate, instruction.move_to)

    def lookup(self, position: int) -> Optional[str]:
        stack = self.stacks[position - 1]
        return None if len(stack) == 0 else stack[-1]


def read_input() -> List[str]:
    with open("input.txt") as f:
        lines = f.readlines()
    return lines


def parse_instruction(line: str) -> Instruction:
    split = line.split(" ")
    assert len(split) == 6
    return Instruction(int(split[1]), int(split[3]), int(split[5]))


def parse_board(lines: List[str]) -> Board:
    size = len(lines[-1].split())
    board = Board(size)
    for line in reversed(lines[:-1]):
        for i, crane in enumerate(line[1::4], 1):
            if crane != " ":
                board.put(crane, i)
    return board


def parse_input(lines: List[str]) -> Tuple[Board, List[Instruction]]:
    board_lines = []
    moves = []
    board_now = True
    for line in lines:
        line = line.removesuffix("\n")
        if len(line) <= 1:
            board_now = False
            continue

        if board_now:
            board_lines.append(line)
        else:
            moves.append(parse_instruction(line))
    board = parse_board(board_lines)
    return board, moves


def simulate_moves(
    board: Board, moves: List[Instruction], mode: Literal[9000, 9001]
) -> None:
    for move in moves:
        if mode == 9000:
            board.apply_9000(move)
        elif mode == 9001:
            board.apply_9001(move)
        else:
            raise ValueError(f"unknown mode {mode}")


def simulate_moves_9001(board: Board, moves: List[Instruction]) -> None:
    for move in moves:
        board.apply(move)


def get_stack_tops(board: Board) -> str:
    msg = ""
    for pos in range(1, board.size + 1):
        top_crane = board.lookup(pos)
        if not top_crane:
            raise ValueError(f"no cranes at position {pos}")
        else:
            msg += top_crane
    return msg


def do_task(board: Board, moves: List[Instruction], mode: Literal[9000, 9001]) -> None:
    simulate_moves(board, moves, mode)
    tops = get_stack_tops(board)
    print(f"top of each stack in mode {mode} is represented as {tops}")


def main():
    input_lines = read_input()
    board, moves = parse_input(input_lines)
    do_task(deepcopy(board), moves, mode=9000)
    do_task(deepcopy(board), moves, mode=9001)


if __name__ == "__main__":
    main()
