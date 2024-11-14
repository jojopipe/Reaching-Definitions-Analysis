from sys import exception
from typing import List
from variable import Variable


__block_type = ["COMPARE", "ASSIGN", "SKIP"]

class Block:
    label: int
    content = 0
    block_type: int
    overriding_variables: List[Variable]

    def __init__(self, label: int, block_type: int, overrides: List[Variable]):
        self.label = label
        if not block_type in range(0,2):
            raise Exception(f"block type {block_type} is not in range [0,2]")
        self.block_type = block_type
        self.overriding_variables = overrides

pass