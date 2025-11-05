import sys
import argparse
from pyrosetta import *
pyrosetta.init(extra_options="-out:levels core.pack.interaction_graph.interaction_graph_factory:warnings core.pack.pack_rotamers:warnings  ")
import random
from pyrosetta.rosetta import core
from pyrosetta.rosetta import protocols
from pyrosetta.rosetta.core.scoring.dssp import Dssp



def identify_secondary_structure_spans(ss):
    out=[]
    for s in range(len(ss)):
        if ss[s]!= "H" and ss[s]!="E":
            continue
        else:
            if s == 0 or ss[s] != ss[s - 1]:
                start=s+1
            if s == len(ss) - 1 or ss[s + 1] != ss[s]:
                end=s+1
                out.append((start,end))
    return out


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     #add line here to add an argument
#     parser.add_argument("structure", help="Path to the input PDB file")
#     args = parser.parse_args()
#     mypose = pose_from_pdb(args.structure)

#     dssp = Dssp(mypose)
#     ss = dssp.get_dssp_secstruct()
#     print(ss)

    # ss= "   EEEEE   HHHHHHHH  EEEEE   IGNOR EEEEEE   HHHHHHHHHHH  EEEEE  HHHH   "
    # testing=identify_secondary_structure_spans(ss)
    # print(testing)


#     # for s in range(len(ss)):
#     #     print(ss[s])

