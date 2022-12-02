from typing import List


def read_input() -> List[str]:
    with open("input.txt") as f:
        lines = f.readlines()
    return lines


def process_input(lines: List[str]) -> List[List[int]]:
    elves_calories_lists: List[List[int]] = [[]]
    for line in lines:
        if line == "\n":
            elves_calories_lists.append([])
        else:
            calorie = int(line)
            elves_calories_lists[-1].append(calorie)
    return elves_calories_lists


def get_calorie_sums(calorie_lists: List[List[int]]) -> List[int]:
    return [sum(calorie_list) for calorie_list in calorie_lists]


def main():
    input_lines = read_input()
    calorie_lists = process_input(input_lines)
    calorie_sums = get_calorie_sums(calorie_lists)
    # NOTE: pt. one
    max_calories = max(calorie_sums)
    print(f"max carried calories: {max_calories}")

    # NOTE: pt. two
    top_three = sum(sorted(calorie_sums)[-3:])
    print(f"top three carried calories: {top_three}")


if __name__ == "__main__":
    main()
