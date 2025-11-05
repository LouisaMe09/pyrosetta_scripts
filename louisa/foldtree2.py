from pyrosetta.rosetta.core.kinematics import FoldTree
from get_secondary_struct import identify_secondary_structure_spans


def internal_loop_positions(ss: str):
    """
    Gibt nur Loop-Regionen (L oder ' ') zurück, die zwischen
    Sekundärstrukturelementen (H/E) liegen.
    Rückgabe: Liste von (start, end) Tupeln (1-basiert)
    """
    loop = {"L", " "}
    sec = {"H", "E"}
    n = len(ss)
    out = []
    i = 0

    while i < n:
        if ss[i] not in loop:
            i += 1
            continue

        j = i
        while j + 1 < n and ss[j + 1] in loop:
            j += 1

        left_is_sec = (i - 1 >= 0 and ss[i - 1] in sec)
        right_is_sec = (j + 1 < n and ss[j + 1] in sec)

        if left_is_sec and right_is_sec:
            out.append((i + 1, j + 1))  # 1-basiert

        i = j + 1

    return out


def get_mid_positions(pos):
    return [int((start + end) / 2) for start, end in pos]


def jump_edges(ft, first_sec, midpoints, start_label=1):
    """
    Fügt Jump-Kanten hinzu, wobei die Label fortlaufend
    über mehrere Aufrufe weitergezählt werden.
    """
    n = start_label
    first_mid = midpoints[0]

    if first_sec == first_mid:
        for mid in midpoints[1:]:
            ft.add_edge(first_sec, mid, n)
            n += 1
    else:
        for mid in midpoints:
            ft.add_edge(first_sec, mid, n)
            n += 1

    return n  # Rückgabe: nächstes verfügbares Label


def peptide_edges_loops(ft, mid_positions, outer_positions):
    for (start, end), mid in zip(outer_positions, mid_positions):
        if mid != start:
            ft.add_edge(mid, start, -1)
        if mid != end:
            ft.add_edge(mid, end, -1)


def peptide_edges_secondary(ft, mid_positions, outer_positions, nres):
    """
    SS peptide edges with special ends:
      - first SS midpoint -> 1  (backwards)
      - last  SS midpoint -> nres (forwards)
      - others use their own (start, end)
    """
    m = len(mid_positions)
    for idx, ((start, end), mid) in enumerate(zip(outer_positions, mid_positions)):
        left = 1 if idx == 0 else start
        right = nres if idx == m - 1 else end

        if mid != left:
            ft.add_edge(mid, left, -1)
        if mid != right:
            ft.add_edge(mid, right, -1)


def fold_tree_from_dssp_string(seq):
    ft = FoldTree()
    nres = len(seq)

    secondary_pos = identify_secondary_structure_spans(seq)
    loop_pos = internal_loop_positions(seq)
    mid_sec_pos = get_mid_positions(secondary_pos)
    mid_loop_pos = get_mid_positions(loop_pos)
    first_sec_mid_pos = mid_sec_pos[0]

    # Label fortlaufend zählen
    label_counter = 1
    label_counter = jump_edges(ft, first_sec_mid_pos, mid_sec_pos, label_counter)
    label_counter = jump_edges(ft, first_sec_mid_pos, mid_loop_pos, label_counter)

    peptide_edges_loops(ft, mid_loop_pos, loop_pos)
    peptide_edges_secondary(ft, mid_sec_pos, secondary_pos, nres)

    # Sammle alle Edges zum Debuggen
    all_edges = []
    for i in range(1, nres + 1):
        try:
            outgoing = ft.get_outgoing_edges(i)
            for e in outgoing:
                edge_tuple = (e.start(), e.stop())
                if edge_tuple not in all_edges:
                    all_edges.append(edge_tuple)
        except RuntimeError:
            continue

    # # 🧩 Debug-Check
    # print(f"Num jumps: {ft.num_jump()} | Biggest label: {ft.biggest_label()}")
    # print(f"Total edges: {ft.num_edges()}")

    return ft, all_edges


# 🧪 Test mit Beispiel-Sequenz
# seq = "   EEEEEEE    EEEEEEE         EEEEEEEEE    EEEEEEEEEE   HHHHHH         EEEEEEEEE         EEEEE     "
# ft, edges = fold_tree_from_dssp_string(seq)

# print("\n✅ All edges (start, stop, label):")
# for e in edges:
#     typ = "Jump" if e[2] > 0 else "Peptide"
#     print(f"{typ:8s} {e[0]:3d} → {e[1]:3d}")
