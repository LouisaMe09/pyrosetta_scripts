import sys
import argparse
import random
from pyrosetta import *
pyrosetta.init(extra_options="-out:levels core.pack.interaction_graph.interaction_graph_factory:warnings core.pack.pack_rotamers:warnings")
from pyrosetta.rosetta import core
from pyrosetta.rosetta import protocols
from pyrosetta.rosetta.protocols.moves import Mover
from pyrosetta.rosetta.core.scoring import attributes_for_parse_score_function_w_description
from pyrosetta.rosetta.utility.tag import (
    XMLSchemaAttribute,
    XMLSchemaDefinition,
    list_utility_tag_XMLSchemaAttribute_t,
    XMLSchemaType
)
from pyrosetta.rosetta.core.scoring import attributes_for_parse_score_function_w_description
from pyrosetta.rosetta.protocols import moves


class BootcampMover(Mover):
    """A simple example Mover that randomly perturbs backbone angles (phi/psi)
    and uses a Monte Carlo accept/reject scheme to minimize energy.
    """

    clones = []  # class-level reference to keep cloned movers alive

    def __init__(self, sxfn=None, nr_iter=1000, min_phi=-10, max_phi=10, min_psi=-10, max_psi=10):
        super().__init__()
        self.nr_iter_ = nr_iter
        self.min_phi_ = min_phi
        self.max_phi_ = max_phi
        self.min_psi_ = min_psi
        self.max_psi_ = max_psi
        self.sfxn_ = sxfn if sxfn is not None else get_fa_scorefxn()

    # --- Setter & Getter ---
    def set_nr_iter(self, nr_iter): self.nr_iter_ = nr_iter
    def get_nr_iter(self): return self.nr_iter_

    def set_min_phi(self, value): self.min_phi_ = value
    def get_min_phi(self): return self.min_phi_

    def set_max_phi(self, value): self.max_phi_ = value
    def get_max_phi(self): return self.max_phi_

    def set_min_psi(self, value): self.min_psi_ = value
    def get_min_psi(self): return self.min_psi_

    def set_max_psi(self, value): self.max_psi_ = value
    def get_max_psi(self): return self.max_psi_

    def set_sfxn(self, sfxn): self.sfxn_ = sfxn
    def get_sfxn(self): return self.sfxn_

    # --- Core method: apply() ---
    def apply(self, pose):
        """Perform random backbone perturbations with Monte Carlo acceptance."""
        nr_res = pose.total_residue()
        scorefxn = self.sfxn_
        mc = protocols.moves.MonteCarlo(pose, scorefxn, 1.0)

        movemap = core.kinematics.MoveMap()
        movemap.set_bb(True)
        movemap.set_chi(True)

        # Minimization setup
        min_opts = core.optimization.MinimizerOptions("lbfgs_armijo_atol", 0.01, True)
        minimizer = core.optimization.AtomTreeMinimizer()


        mc_trials = 0
        mc_accepted = 0

        for i in range(1, self.nr_iter_ + 1):
            randres = random.randint(1, nr_res)
            phi_pert = random.uniform(self.min_phi_, self.max_phi_)
            psi_pert = random.uniform(self.min_psi_, self.max_psi_)

            pose.set_phi(randres, pose.phi(randres) + phi_pert)
            pose.set_psi(randres, pose.psi(randres) + psi_pert)

            tf = core.pack.task.TaskFactory()
            task = tf.create_task_and_apply_taskoperations(pose)
            task.restrict_to_repacking()

            packer = protocols.minimization_packing.PackRotamersMover(scorefxn, task)
            packer.apply(pose)

            minimizer.run(pose, movemap, scorefxn, min_opts)

            accepted = mc.boltzmann(pose)
            mc_trials += 1
            if accepted:
                mc_accepted += 1

            if i % 100 == 0:
                acc_rate = mc_accepted / mc_trials
                print(f"Step {i}: acceptance rate = {acc_rate:.2f}")

        mc.recover_low(pose)
        # print(f"✅ Final score: {scorefxn(pose):.3f}")

    # --- RosettaScripts interface ---
    def get_name(self):
        return self.__class__.__name__

    @staticmethod
    def mover_name():
        return "BootcampMover"

    def parse_my_tag(self, tag, datamap):
        """Extract parameters from RosettaScripts XML tag."""
        # Number of iterations
        if tag.hasOption("num_iterations"):
            iters = tag.getOptionInt("num_iterations")
            self.set_nr_iter(iters)

        # Scorefunction
        if tag.hasOption("scorefxn"):
            scorefxn_name = tag.getOptionStr("scorefxn")
            sfxn = core.scoring.parse_score_function(scorefxn_name, datamap)
            self.set_sfxn(sfxn)

        if tag.hasOption("min_phi"):
            min_phi = tag.getOptionReal("min_phi")
            self.set_min_phi(min_phi)

        if tag.hasOption("max_phi"):
            max_phi = tag.getOptionReal("max_phi")
            self.set_max_phi(max_phi)

        if tag.hasOption("min_psi"):
            min_psi = tag.getOptionReal("min_psi")
            self.set_min_psi(min_psi)

        if tag.hasOption("max_psi"):
            max_psi = tag.getOptionReal("max_psi")
            self.set_max_psi(max_psi)


    @staticmethod
    def provide_xml_schema(xsd):
        """Describe the XML interface for BootCampMover."""
        # Leere Liste für Attribute erstellen
        attrs = list_utility_tag_XMLSchemaAttribute_t()

        # 2️⃣ num_iterations
        attrs.append(
            XMLSchemaAttribute(
                "num_iterations",
                "Number of Monte Carlo iterations to perform.",
                XMLSchemaType.xsct_non_negative_integer
            )
        )

        # 3️⃣ min_phi / max_phi
        attrs.append(
            XMLSchemaAttribute(
                "min_phi",
                "Minimum random perturbation (degrees) applied to backbone φ angle.",
                XMLSchemaType.xsct_real
            )
        )
        attrs.append(
            XMLSchemaAttribute(
                "max_phi",
                "Maximum random perturbation (degrees) applied to backbone φ angle.",
                XMLSchemaType.xsct_real
            )
        )

        # 4️⃣ min_psi / max_psi
        attrs.append(
            XMLSchemaAttribute(
                "min_psi",
                "Minimum random perturbation (degrees) applied to backbone ψ angle.",
                XMLSchemaType.xsct_real
            )
        )
        attrs.append(
            XMLSchemaAttribute(
                "max_psi",
                "Maximum random perturbation (degrees) applied to backbone ψ angle.",
                XMLSchemaType.xsct_real
            )
        )

        # 5️scorefxn 
        attributes_for_parse_score_function_w_description(
            attrs,
            "ScoreFunction to use for evaluating and accepting moves."
        )

        # 6 Alles registrieren mit Beschreibung
        moves.xsd_type_definition_w_attributes(
            xsd,
            "BootCampMover",
            "Performs random φ/ψ backbone perturbations, "
            "followed by sidechain repacking and minimization, "
            "accepting or rejecting moves using a Monte Carlo criterion.",
            attrs
        )