from typing import List
from block import Block

class Graph:
    reaching_map: List[List[int]]
    initialBlock: int
    finalBlocks: List[int]

    def __init__(self, reaching_map: List[List[int]], initialBlock: int, finalBlocks: List[int]) -> None:
        self.reaching_map = reaching_map
        self.initialBlock = initialBlock
        self.finalBlocks = finalBlocks

pass