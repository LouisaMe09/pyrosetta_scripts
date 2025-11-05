from foldtree2 import *

edges = [
    (7, 1),
    (7, 10),
    (7, 12),
    (12, 11),
    (12, 14),
    (7, 18),
    (18, 15),
    (18, 21),
    (7, 26),
    (26, 22),
    (26, 30),
    (7, 35),
    (35, 31),
    (35, 39),
    (7, 41),
    (41, 40),
    (41, 43),
    (7, 48),
    (48, 44),
    (48, 53),
    (7, 55),
    (55, 54),
    (55, 56),
    (7, 59),
    (59, 57),
    (59, 62),
    (7, 67),
    (67, 63),
    (67, 71),
    (7, 76),
    (76, 72),
    (76, 80),
    (7, 85),
    (85, 81),
    (85, 89),
    (7, 92),
    (92, 90),
    (92, 99)
]

seq="   EEEEEEE    EEEEEEE         EEEEEEEEE    EEEEEEEEEE   HHHHHH         EEEEEEEEE         EEEEE     "

def test_foldtree_output():
    ft, result_edges = fold_tree_from_dssp_string(seq)
    assert sorted(result_edges) == sorted(edges)
