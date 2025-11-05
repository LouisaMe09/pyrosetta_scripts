import sys
import argparse
from pyrosetta import *
pyrosetta.init(extra_options="-out:levels core.pack.interaction_graph.interaction_graph_factory:warnings core.pack.pack_rotamers:warnings  ")
import random
from pyrosetta.rosetta import core
from pyrosetta.rosetta import protocols
From pyrosetta.rosetta.protocols.moves import Mover


class BootcampMover(Mover):

    clones=[]
    
    def __init__(self, nr_iter=1000, min_phi=-10, max_phi=10, min_psi=-10, max_psi=10):
        super().__init__()
        self.nr_iter = nr_iter
        self.min_phi = min_phi
        self.max_phi = max_phi
        self.min_psi = min_psi
        self.max_psi = max_psi

    def apply(self, pose):
        pose = pose.get()

        nr_res = pose.total_residue()
        scorefxn = get_fa_scorefxn()
        mc = protocols.moves.MonteCarlo(pose, scorefxn, 1.0)

        movemap = core.kinematics.MoveMap()
        movemap.set_bb(True)
        movemap.set_chi(True)

        mc_trials = 0
        mc_accepted = 0

        for i in range(1, self.nr_iter + 1):
            randres = random.randint(1, nr_res)
            phi_pert = random.uniform(self.min_phi, self.max_phi)
            psi_pert = random.uniform(self.min_psi, self.max_psi)

            pose.set_phi(randres, pose.phi(randres) + phi_pert)
            pose.set_psi(randres, pose.psi(randres) + psi_pert)

            accepted = mc.boltzmann(pose)
            mc_trials += 1
            if accepted:
                mc_accepted += 1

            if i % 100 == 0:
                print(f"Step {i}: acceptance rate = {mc_accepted/mc_trials:.2f}")

        mc.recover_low(pose)
        print(f"\n✅ Final score: {scorefxn(pose):.3f}")

    def get_name(self):
        return self.__class__.__name__