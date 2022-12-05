from typing import List, Tuple


class Assignment:
    def __init__(self, left: int, right: int):
        self.left = left
        self.right = right

    def contains(self, other: "Assignment") -> bool:
        return self.left <= other.left and other.right <= self.right

    def overlaps_with(self, other: "Assignment") -> bool:
        def overlaps_from_the_left(a: Assignment, b: Assignment) -> bool:
            # a is on the left side of b
            return a.left <= b.left and b.left <= a.right

        return overlaps_from_the_left(self, other) or overlaps_from_the_left(
            other, self
        )

    @staticmethod
    def from_raw(raw: str) -> "Assignment":
        left_str, right_str = raw.split("-")
        return Assignment(int(left_str), int(right_str))


def read_input() -> List[str]:
    with open("input.txt") as f:
        lines = f.readlines()
    return lines


def get_assignment_pairs(lines: List[str]) -> List[Tuple[Assignment, Assignment]]:
    result: List[Tuple[Assignment, Assignment]] = []
    for line in lines:
        first, second = line.removesuffix("\n").split(",")
        result.append((Assignment.from_raw(first), Assignment.from_raw(second)))
    return result


def fully_overlap(a: Assignment, b: Assignment) -> bool:
    return a.contains(b) or b.contains(a)


def count_containing_pairs(pairs: List[Tuple[Assignment, Assignment]]) -> int:
    return sum(fully_overlap(a, b) for a, b in pairs)


def count_overlapping_pairs(pairs: List[Tuple[Assignment, Assignment]]) -> int:
    return sum(a.overlaps_with(b) for a, b in pairs)


def main():
    input_lines = read_input()
    pairs = get_assignment_pairs(input_lines)
    no_fully = count_containing_pairs(pairs)
    no_partially = count_overlapping_pairs(pairs)
    print(f"number of fully overlapping pairs is {no_fully}")
    print(f"number of partially overlapping pairs is {no_partially}")


if __name__ == "__main__":
    main()
