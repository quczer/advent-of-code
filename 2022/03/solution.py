from typing import List, Optional, Set, Tuple, TypeVar

X = TypeVar("X")


def read_input() -> List[str]:
    with open("input.txt") as f:
        lines = f.readlines()
    return lines


def process_input_first(lines: List[str]) -> Tuple[List[List[str]], List[List[str]]]:
    backpacks_a = []
    backpacks_b = []
    for line in lines:
        backpacks = list(line.removesuffix("\n"))
        half_len = len(backpacks) // 2
        a, b = backpacks[:half_len], backpacks[half_len:]
        backpacks_a.append(a)
        backpacks_b.append(b)
    return backpacks_a, backpacks_b


def process_input_second(lines: List[str]) -> List[List[str]]:
    backpacks = []
    for line in lines:
        backpack = list(line.removesuffix("\n"))
        backpacks.append(backpack)
    return backpacks


def fold(xs: List[X], n: int) -> List[List[X]]:
    assert len(xs) % n == 0
    result = []
    for i in range(0, len(xs), n):
        result.append(xs[i : i + n])
    return result


def get_priority(letter: str) -> int:
    ord_ = ord(letter)
    if ord_ < ord("a"):  # uppercase - ord('a') == 97; ord('A') == 65
        return ord_ - ord("A") + 27
    else:  # lowercase
        return ord_ - ord("a") + 1


def get_intersection(
    xs: List[str], ys: List[str], zs: Optional[List[str]] = None
) -> Set[str]:
    result = set(xs).intersection(ys)
    if zs:
        result = result.intersection(zs)
    return result


def calc_priority_sum_first(
    backpacks_a: List[List[str]], backpacks_b: List[List[str]]
) -> int:
    priority_sum = 0
    for a, b in zip(backpacks_a, backpacks_b):
        intersection = get_intersection(a, b)
        for letter in intersection:
            priority_sum += get_priority(letter)
    return priority_sum


def calc_priority_sum_second(backpack_groups: List[List[List[str]]]) -> int:
    priority_sum = 0
    for elf1, elf2, elf3 in backpack_groups:
        badge = get_intersection(elf1, elf2, elf3).pop()
        priority_sum += get_priority(badge)
    return priority_sum


def solve_first(input_lines: List[str]) -> None:
    backpacks_a, backpacks_b = process_input_first(input_lines)
    priority_sum = calc_priority_sum_first(backpacks_a, backpacks_b)
    print(f"(1) overall priority sum is {priority_sum}")


def solve_second(input_lines: List[str]) -> None:
    backpacks = process_input_second(input_lines)
    backpacks_groups = fold(backpacks, 3)
    priority_sum = calc_priority_sum_second(backpacks_groups)
    print(f"(2) overall badge priority sum is {priority_sum}")


def main():
    input_lines = read_input()
    solve_first(input_lines)
    solve_second(input_lines)


if __name__ == "__main__":
    main()
