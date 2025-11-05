import argparse
from pyrosetta import init, pose_from_pdb
from pyrosetta.rosetta import core
from pyrosetta.rosetta import protocols
from pyrosetta.rosetta.core.scoring.dssp import Dssp
# from pyrosetta.rosetta.core.scoring.dssp import DSSP
from pyrosetta.rosetta.core.pose import Pose
from foldtree2 import fold_tree_from_dssp_string  # dein Modul!

def main():
    # 1️⃣ Argumentparser: PDB-Datei einlesen
    parser = argparse.ArgumentParser(description="Generate FoldTree from PDB using DSSP")
    parser.add_argument("structure", help="Path to the input PDB file")
    args = parser.parse_args()

    # 2️⃣ Rosetta initialisieren
    init()

    # 3️⃣ Pose aus PDB erstellen
    pose = pose_from_pdb(args.structure)
    print(f"✅ Loaded PDB with {pose.size()} residues")

    # 4️⃣ DSSP anwenden → Sekundärstrukturstring
    dssp = Dssp(pose)
    ss = dssp.get_dssp_secstruct()
    print("✅ Secondary structure string:")
    print(ss)
    print()

    # 5️⃣ Deinen FoldTree aus der DSSP-String berechnen
    ft, edges = fold_tree_from_dssp_string(ss)
    print("✅ Generated FoldTree edges:")
    for e in edges:
        print(f"   {e[0]:3} → {e[1]:3}")

    if ft.check_fold_tree():
        print("✅ FoldTree structure is internally valid")
    else:
        print("❌ FoldTree object itself is invalid – not setting it on pose!")
    return  # oder raise

    # 6️⃣ FoldTree auf Pose setzen
    pose.fold_tree(ft)
    print("\n✅ FoldTree set on pose")

    # 7️⃣ Validierung
    if pose.fold_tree().check_fold_tree():
        print("🎉 FoldTree is valid!")
    else:
        print("❌ FoldTree invalid!")

    # Optional: Ausgabe der Edges aus der Pose
    print("\nFoldTree details:")
    for i in range(1, ft.num_edge() + 1):
        e = ft.edge(i)
        edge_type = "Jump" if e.label() > 0 else "Peptide"
        print(f"{i:2d}: {edge_type:8s} {e.start():3} → {e.stop():3} (label={e.label():>2})")


if __name__ == "__main__":
    main()
