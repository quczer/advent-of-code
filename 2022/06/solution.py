from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional


class Counter:
    def __init__(self, items: Optional[Iterable] = None):
        self.items: Dict[Any, int] = defaultdict(lambda: 0)
        if items:
            for item in items:
                self.add(item)

    def add(self, x) -> None:
        self.items[x] += 1

    def remove(self, x) -> None:
        self.items[x] -= 1
        if self.items[x] == 0:
            self.items.pop(x)  # this line is important; garbage collecting

    @property
    def size(self) -> int:
        return len(self.items)

    def __repr__(self) -> str:
        return f"Counter: {dict.__repr__(self.items)}, size = {self.size}"

    def __len__(self) -> str:  # don't need it; purely educational
        return repr(self)


def read_input() -> List[str]:
    with open("input.txt") as f:
        lines = f.readlines()
    return lines


def parse_input(lines: List[str]) -> List[str]:
    return list(lines[0].removesuffix("\n"))


def find_packet_start_slow(message: List[str], window_len: int) -> Optional[int]:
    """complexity = O(WINDOW_LEN * len(message))"""
    for i in range(len(message) - window_len):
        letters = Counter(message[i : i + window_len])
        if letters.size == window_len:  # different letters
            return i + window_len
    return None


def find_packet_start_fast(message: List[str], window_len: int) -> Optional[int]:
    """complexity = O(len(message))"""
    letters = Counter(message[:window_len])
    if letters.size == window_len:  # different letters
        return 1
    for i in range(window_len, len(message)):
        letters.remove(message[i - window_len])
        letters.add(message[i])
        if letters.size == window_len:  # different letters
            return i + 1
    return None


def solve(message: List[str], window_len: int) -> None:
    packet_start = find_packet_start_slow(message, window_len)
    assert packet_start == find_packet_start_slow(message, window_len)
    print(f"found packet start for window of length {window_len} is {packet_start}")


def main():
    input_lines = read_input()
    message = parse_input(input_lines)
    solve(message, window_len=4)
    solve(message, window_len=14)


if __name__ == "__main__":
    main()
