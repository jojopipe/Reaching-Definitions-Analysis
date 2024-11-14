from vb_pair import VBPair
from typing import List

class TransferFunction:
    kill: List[VBPair]
    gen: List[VBPair]

    def __init__(self, kill: List[VBPair], gen: List[VBPair]):
        self.kill = kill
        self.gen = gen

def apply_transfer_function(x: List[VBPair], f: TransferFunction):
    new_x = []
    for elem in x:
        if elem not in f.kill:
            new_x.append(elem)
    for elem in f.gen:
        if elem not in new_x:
            new_x.append(elem)
    return new_x