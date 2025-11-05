from pyrosetta.rosetta.core.kinematics import FoldTree
from get_secondary_struct import identify_secondary_structure_spans



# def loop_positions(ss):
#     out = []
#     for s in range(len(ss)):
#         if ss[s] not in ["L", " "]:
#             continue
#         else:
#             if s == 0 or ss[s] != ss[s - 1]:
#                 start = s + 1
#             if s == len(ss) - 1 or ss[s + 1] != ss[s]:
#                 end = s + 1
#                 # Check: links oder rechts angrenzend an H oder E?
#                 left_is_sec = (start > 1 and ss[start - 2] in ["H", "E"])
#                 right_is_sec = (end < len(ss) and ss[end] in ["H", "E"])
#                 if left_is_sec or right_is_sec:
#                     out.append((start, end))
#     return out


# def identify_secondary_structure_spans(ss):
#     out=[]
#     for s in range(len(ss)):
#         if ss[s]!= "H" and ss[s]!="E":
#             continue
#         else:
#             if s == 0 or ss[s] != ss[s - 1]:

                
#                 start=s+1
#             if s == len(ss) - 1 or ss[s + 1] != ss[s]:
#                 end=s+1

#                 out.append((start,end))
#     return out


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
        # Loop-Bereich starten
        if ss[i] not in loop:
            i += 1
            continue

        # gesamten Loop-Block [i..j] finden
        j = i
        while j + 1 < n and ss[j + 1] in loop:
            j += 1

        # check: ist links UND rechts Sekundärstruktur?
        left_is_sec = (i - 1 >= 0 and ss[i - 1] in sec)
        right_is_sec = (j + 1 < n and ss[j + 1] in sec)

        if left_is_sec and right_is_sec:
            out.append((i + 1, j + 1))  # 1-basiert

        i = j + 1

    return out


def get_mid_positions(pos):
    midpoints = [int((start + end) / 2) for start, end in pos]
    return midpoints


def jump_edges(ft, first_sec, midpoints):
    n=1
    first_midpoint=midpoints[0]
    if first_sec==first_midpoint:
        for mid in midpoints[1:]:
            ft.add_edge(first_sec, mid, n)
            n+=1
    else:
        for mid in midpoints:
            ft.add_edge(first_sec, mid, n)
            n+=1

# def peptide_edges(ft, mid_positions, outer_positions):
#     for (start, end), mid in zip(outer_positions, mid_positions):
#         if mid != start:
#             ft.add_edge(mid, start, -1)
#         if mid != end:
#             ft.add_edge(mid, end, -1)


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
        left  = 1    if idx == 0     else start
        right = nres if idx == m - 1 else end

        if mid != left:
            ft.add_edge(mid, left, -1)
        if mid != right:
            ft.add_edge(mid, right, -1)







def fold_tree_from_dssp_string(seq):
    ft = FoldTree()
    secondary_pos=identify_secondary_structure_spans(seq)
    # print(secondary_pos)
    loop_pos=internal_loop_positions(seq)
    # print(loop_pos)
    mid_sec_pos=get_mid_positions(secondary_pos)
    first_sec_mid_pos=mid_sec_pos[0]
    mid_loop_pos=get_mid_positions(loop_pos)

    jump_edges(ft, first_sec_mid_pos, mid_sec_pos)
    jump_edges(ft, first_sec_mid_pos, mid_loop_pos)

    peptide_edges_loops(ft, mid_loop_pos, loop_pos)
    peptide_edges_secondary(ft, mid_sec_pos, secondary_pos, len(seq))


    all_edges = []

    for i in range(1, 101):
        try:
            outgoing = ft.get_outgoing_edges(i)
            for e in outgoing:
                edge_tuple = (e.start(), e.stop())
                if edge_tuple not in all_edges:
                    all_edges.append(edge_tuple)
        except RuntimeError:
            continue

    return ft, all_edges
    # return ft
    

seq="   EEEEEEE    EEEEEEE         EEEEEEEEE    EEEEEEEEEE   HHHHHH         EEEEEEEEE         EEEEE     "
# ex=fold_tree_from_dssp_string(seq)
# print(ex)

# print("All edges in the FoldTree:\n")
# for i in range(1, ex.num_edges() + 1):
#     e = ex.edge(i)
#     edge_type = "Jump" if e.label() > 0 else "Peptide"
#     print(f"{i:2d}: {edge_type:8s}  {e.start():>3} → {e.stop():<3}   (label={e.label()})")

ft = fold_tree_from_dssp_string(seq)
print(ft)
# ------------------------------------------------------------------
# all_edges = []

# #  Wir probieren einfach alle möglichen Residue-IDs, z. B. 1–100
# # (da FoldTree selbst keine Liste der Residues enthält)
# for i in range(1, 101):
#     try:
#         outgoing = ft.get_outgoing_edges(i)
#         for e in outgoing:
#             # Duplikate vermeiden
#             if not any(e.start() == ex.start() and e.stop() == ex.stop() and e.label() == ex.label() for ex in all_edges):
#                 all_edges.append(e)
#     except RuntimeError:
#         # Falls Position i keine gültigen Edges hat → ignorieren
#         continue

# # Ausgabe
# print("All edges in FoldTree:")
# print("=" * 45)
# for i, e in enumerate(all_edges, start=1):
#     edge_type = "Jump" if e.label() > 0 else "Peptide"
#     print(f"{i:2d}: {edge_type:8s}  {e.start():3} → {e.stop():3}  (label={e.label():>2})")
# print("=" * 45)



# all_edges = []

# # Wir probieren einfach alle möglichen Residue-IDs, z. B. 1–100
# for i in range(1, 101):
#     try:
#         outgoing = ft.get_outgoing_edges(i)
#         for e in outgoing:
#             edge_tuple = (e.start(), e.stop(), e.label())
#             if edge_tuple not in all_edges:
#                 all_edges.append(edge_tuple)
#     except RuntimeError:
#         continue

# # Ausgabe als Liste von Tupeln
# print("Edges as tuples:")
# print(all_edges)


# all_edges = []

# # Wir probieren einfach alle möglichen Residue-IDs, z. B. 1–100
# for i in range(1, 101):
#     try:
#         outgoing = ft.get_outgoing_edges(i)
#         for e in outgoing:
#             edge_tuple = (e.start(), e.stop())
#             if edge_tuple not in all_edges:
#                 all_edges.append(edge_tuple)
#     except RuntimeError:
#         continue

# # Ausgabe als Liste von Tupeln
# print("Edges (start, stop):")
# print(all_edges)