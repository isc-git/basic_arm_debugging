from enum import Enum
from typing import List


class ArmState(Enum):
    OK = 0
    ERROR = 1


def print_matrix(elements: List[List[str]]) -> str:
    col_max = [0] * len(elements[0])
    for row in elements:
        for col in range(len(row)):
            if len(row[col]) > col_max[col]:
                col_max[col] = len(row[col])

    mat = ""
    for row in elements:
        row_fixed = []
        for index in range(len(row)):
            row_fixed.append(f"{row[index]:>{col_max[index]}}")

        mat += "│ " + ", ".join(row_fixed) + " │\n"

    return mat
