from typing import List

def flatten(grid: List[List[int]]):
    arr = []
    for row in grid:
        arr.extend(row)
    return arr


def unflatten(arr: List[int], n=9):
    grid = []
    for i in range(0, len(arr), n):
        grid.append(arr[i:i+n])
    return grid


def arr2str(arr: List[int]):
    string = ''
    for digit in arr:
        string += str(digit)
    return string


def str2arr(string: str, blank:str = '.'):
    arr = []
    end = string.find('-')
    end = len(string) if end == -1 else end
    for c in string[0:end]:
        if c == blank:
            arr.append(0)
        else:
            arr.append(int(c))
    return arr  # [int(c) for c in string]


def grid2str(grid: List[List[int]]) -> str:
    return arr2str(flatten(grid))


def str2grid(string: str) -> List[List[int]]:
    return unflatten(str2arr(string))