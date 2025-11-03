import sys
import argparse
from pyrosetta import *

init(extra_options="-ignore_unrecognized_res")

parser = argparse.ArgumentParser()
#add line here to add an argument
parser.add_argument("filename", help="Path to the input PDB file")
args = parser.parse_args()
print(f"The filename passed in is: {args.filename}")
