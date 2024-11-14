from variable import Variable
from block import Block
from graph import Graph
from typing import List
from vb_pair import VBPair
from transfer_function import TransferFunction, apply_transfer_function

def read_data(path: str):
    with open(path, 'r') as file:
        content = file.read().split("\n")
    print(content)

    N = int(content[0])
    v = []
    var_map = {}
    for a, curr_var in enumerate(content[1].split(" ")):
        v.append(Variable(curr_var))
        var_map[curr_var] = a

    b_types = content[2].split(" ")
    b_types = [int(elem) for elem in b_types]

    b_overrides = []

    for a, elem in enumerate(content[3].split(" ")):
        if elem == "-":
            b_overrides.append(None)
            continue
        b_overrides.append([])
        for var in elem.split(","):
            index = var_map[var]
            b_overrides[a].append(v[index])

    reaching_map = []
    for i in range(4, len(content)):
        if content[i] == "-":
            reaching_map.append([])
            continue
        reaching_map.append(
            [int(reach_elem) for reach_elem in content[i].split(" ")]
        )
    return N, v, b_types, b_overrides, reaching_map

def setup_blocks(b_types, b_overrides):
    blocks = []
    for i in range(0, N):
        blocks.append(Block(i, b_types[i], b_overrides[i]))
    return blocks

def setup_vbpairs(v, blocks):
    initial = []
    vb_pairs = []  # variables we care about
    for curr in v:
        vb = VBPair(-1, curr)
        vb_pairs.append(vb)
        initial.append(vb)
    for b in blocks:
        if b.block_type == 1:
            for variable in b.overriding_variables:
                vb_pairs.append(VBPair(b.label, variable))
    vb_pairs.sort()
    return initial, vb_pairs

def make_transfer_functions(N, blocks, vb_pairs):
    transfer_functions = []
    for i in range(0, N):
        kill = []
        gen = []
        if blocks[i].block_type != 1:
            transfer_functions.append(TransferFunction([], []))
            continue
        for variable in blocks[i].overriding_variables:
            for p in vb_pairs:
                if variable == p.variable:
                    kill.append(p)
                    if p.block_label == blocks[i].label:
                        gen.append(p)
        transfer_functions.append(TransferFunction(kill, gen))
    return transfer_functions

def invert_graph(N, block_graph):
    reached_by_map = []
    for _ in range(N):
        reached_by_map.append([])
    for i, elem in enumerate(block_graph):
        for a in elem:
            reached_by_map[a].append(i)
    return reached_by_map

def system_of_equations(N, inverse_graph, transfer_functions):
    x = []
    for i in range(N):
        x.append([])
        if not inverse_graph[i]:
            continue
        for a in inverse_graph[i]:
            x[i].append([a, transfer_functions[a]])
    return x

def unionize_sets(sets: List):
    result = []
    for curr_set in sets:
        for elem in curr_set:
            if elem not in result:
                result.append(elem)
    return result

def kleene_iterations(N, x):
    gs = [[]]
    for i in range(N):
        gs[0].append([])
    kleene_index = 1
    while kleene_index < N * N:
        gs.append([])
        for _ in range(N):
            pass
            # gs[kleene_index].append([])

        for i in range(N):
            if not x[i]:
                gs[kleene_index].append(initial)
                continue
            working_sets = []
            for fun in x[i]:
                working_sets.append(apply_transfer_function(gs[kleene_index - 1][fun[0]], fun[1]))
            gs[kleene_index].append(unionize_sets(working_sets))

        if gs[kleene_index] == gs[kleene_index - 1]:
            print(f"found fixed point after {kleene_index} iterations.")
            break

        kleene_index += 1
    return gs

def print_kleene(gs):
    empty = "∅"
    for a, elem in enumerate(gs):
        output = f"{a}: "
        for set in elem:
            if not set:
                output += f"{empty},    "
                continue
            output += "{"
            for vb in set:
                if type(vb) != VBPair:
                    continue
                name = vb.variable.name
                label = vb.block_label
                output += f"({name}, {label}), "
            output = output[:-2]
            output += "},    "
        output = output[:-5]
        print(f"{output}\n")

if __name__ == "__main__":
    path = input("enter path to data: ")
    N, v, b_types, b_overrides, block_graph = read_data(path)
    blocks = setup_blocks(b_types, b_overrides)
    initial, vb_pairs = setup_vbpairs(v, blocks)
    transfer_functions = make_transfer_functions(N, blocks, vb_pairs)
    inverse_graph = invert_graph(N, block_graph)
    x = system_of_equations(N, inverse_graph, transfer_functions)
    gs = kleene_iterations(N, x)

    print_kleene(gs)
    print(f"smallest fixed point at {len(gs)-2} iterations.")