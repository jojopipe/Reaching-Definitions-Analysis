from variable import Variable

class VBPair:
    block_label: int
    variable: Variable

    def __init__(self, block_label: int, variable: Variable):
        self.block_label = block_label
        self.variable = variable

    def __lt__(self, other):
        if self.variable.name == other.variable.name:
            return self.block_label < other.block_label
        return self.variable.name < other.variable.name


pass