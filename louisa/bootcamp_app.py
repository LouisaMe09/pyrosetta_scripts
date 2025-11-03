import sys
import argparse
from pyrosetta import *

init(extra_options="-ignore_unrecognized_res")

parser = argparse.ArgumentParser()
#add line here to add an argument
parser.add_argument("structure", help="Path to the input PDB file")
args = parser.parse_args()
mypose = pose_from_pdb(args.structure)
nr_res=mypose.total_residue()
print(f"{args.structure} has {nr_res} residues")
