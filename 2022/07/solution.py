# requires python 3.10 because of structural pattern matching!
# this one is used frequently - in class X you can type using X not "X"

from __future__ import annotations

from typing import Dict, List

INF = 100_000_000


class Dir:
    def __init__(self, name: str, parent: Dir | None = None):
        if parent is None:  # if we don't provide a parent then we are the root
            self.parent = self
            self.root = self
            self.level = 0
        else:
            self.root = parent.root
            self.parent = parent
            self.level = parent.level + 1

        self.subdirs: Dict[str, Dir] = {}
        self.files: Dict[str, int] = {}
        self.name = name

        self._files_size = 0
        self._dirs_size = 0

    def adjust_size(self, size_delta: int) -> None:
        self._dirs_size += size_delta
        if self.parent != self:
            self.parent.adjust_size(size_delta)

    def add_dir(self, dir: Dir) -> None:
        self.subdirs[dir.name] = dir
        self.parent.adjust_size(dir.size)

    def get_dir(self, dir_name: str) -> Dir | None:
        return self.subdirs.get(dir_name, None)

    def add_file(self, file_name: str, size: int) -> None:
        self.files[file_name] = size
        self._files_size += size
        self.parent.adjust_size(size)

    def __repr__(self) -> str:

        indent = "  "
        result = indent * self.level + f"- {self.name}:"
        for file_name, size in self.files.items():
            result += f"\n{indent * (self.level+1)}- {size} {file_name}"
        for dir in self.subdirs.values():
            result += f"\n{dir}"

        return result

    @property
    def size(self) -> int:
        return self._files_size + self._dirs_size


def read_input() -> List[str]:
    with open("input.txt") as f:
        lines = f.readlines()
    return lines


def parse_input(lines: List[str]) -> List[List[str]]:
    return [line.split() for line in lines]


def try_create_dir(current: Dir, new_name: str) -> Dir:
    next_dir = current.get_dir(new_name)
    if next_dir is None:
        next_dir = Dir(new_name, parent=current)
        current.add_dir(next_dir)
    return next_dir


def build_tree(outputs: List[List[str]]) -> Dir:
    root = Dir("/", parent=None)
    current_dir = root
    for output in outputs:
        match output:
            case ["$", "cd", "/"]:
                current_dir = root
            case ["$", "cd", ".."]:
                current_dir = current_dir.parent
            case ["$", "cd", dir_name]:
                current_dir = try_create_dir(current_dir, dir_name)
            case ["$", "ls"]:
                pass
            case ["dir", dir_name]:
                try_create_dir(current_dir, dir_name)
            case [size, file_name]:
                current_dir.add_file(file_name, int(size))
            case _:
                raise ValueError(f"unknown command {output}")
    return root


def find_light_dirs(current: Dir, max_dir_size: int) -> List[Dir]:
    result = []
    if current.size <= max_dir_size:
        result.append(current)
    for child in current.subdirs.values():
        result.extend(find_light_dirs(child, max_dir_size))
    return result


def find_lightest_heavier_than(current: Dir, min_dir_size: int) -> Dir | None:
    if current.size >= min_dir_size:
        best_size, best_dir = current.size, current
    else:
        best_size, best_dir = INF, None
    for child in current.subdirs.values():
        child_best = find_lightest_heavier_than(child, min_dir_size)
        if child_best is not None and child_best.size < best_size:
            best_size, best_dir = child_best.size, child_best
    return best_dir


def main():
    input_lines = read_input()
    outputs = parse_input(input_lines)
    root = build_tree(outputs)
    light_dirs = find_light_dirs(root, 100_000)
    sum_light_dirs = sum(dir.size for dir in light_dirs)
    print(root)  # uncomment if you want to see the structure
    print(f"found {len(light_dirs)} light dirs, sum of their sizes is {sum_light_dirs}")

    space_missing = 30_000_000 - (70_000_000 - root.size)
    best_to_remove = find_lightest_heavier_than(root, space_missing)

    print(
        f"root weighs {root.size:_}, needed {space_missing:_}, best to remove {best_to_remove.name} of size {best_to_remove.size:_}"
    )


if __name__ == "__main__":
    main()
