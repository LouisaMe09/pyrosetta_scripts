import sys
import argparse
from pyrosetta import *
pyrosetta.init(extra_options="-out:levels core.pack.interaction_graph.interaction_graph_factory:warnings core.pack.pack_rotamers:warnings  ")
import random
from pyrosetta.rosetta import core
from pyrosetta.rosetta import protocols

# init(extra_options="-ignore_unrecognized_res")


parser = argparse.ArgumentParser()
#add line here to add an argument
parser.add_argument("structure", help="Path to the input PDB file")
args = parser.parse_args()
mypose = pose_from_pdb(args.structure)

the_observer = protocols.moves.AddPyMOLObserver(mypose)
the_observer.pymol().apply(mypose)

nr_res=mypose.total_residue()
scorefxn = get_fa_scorefxn()
score = scorefxn(mypose)
mc = MonteCarlo(mypose, scorefxn, 1.0)   
# picking a random number
# Ch
#monte carlo initial
# Set up MoveMap for backbone and sidechain movement
# --- Setup (außerhalb der Schleife) ---
movemap = core.kinematics.MoveMap()
movemap.set_bb(True)
movemap.set_chi(True)

min_opts = core.optimization.MinimizerOptions("lbfgs_armijo_atol", 0.01, True)
minimizer = core.optimization.AtomTreeMinimizer()

print(f"Initial score: {scorefxn(mypose):.3f}")


mc_trials=0
mc_accepted=0
scores=[]

for i in range(1, 1001):  
    randres = random.randint(1, nr_res)

    
    phi_pert = random.uniform(-10, 10)   
    psi_pert = random.uniform(-10, 10)
    orig_phi = mypose.phi(randres)
    orig_psi = mypose.psi(randres)
    mypose.set_phi(randres, orig_phi + phi_pert)
    mypose.set_psi(randres, orig_psi + psi_pert)

    score_after_perturb = scorefxn(mypose)
    # print(f"\nStep {i}: residue {randres}")
    # print(f"  After perturbation: {score_after_perturb:.3f}")

 
    tf = core.pack.task.TaskFactory()
    task = tf.create_task_and_apply_taskoperations(mypose)
    task.restrict_to_repacking()
    core.pack.pack_rotamers(mypose, scorefxn, task)

   
    score_after_pack = scorefxn(mypose)
    # print(f"  After repacking: {score_after_pack:.3f}")

    # minimizer.run(mypose, movemap, scorefxn, min_opts)

    # score_after_min = scorefxn(mypose)
    # print(f"  After minimization: {score_after_min:.3f}")

 
    accepted = mc.boltzmann(mypose)
    mc_trials+=1
    scores.append(score_after_pack)
    if accepted:
        mc_accepted+=1
    

    if i % 100 ==0:
        print(f"acceptance rate: {mc_accepted/mc_trials}")
        print(f"average score:{sum(scores)/len(scores)}")
 
    # print(f"  Accepted? {'Yes' if accepted else 'No'}")
    # print(f"  Current Monte Carlo score: {scorefxn(mypose):.3f}")

# --- Nach der Schleife: bestes Ergebnis wiederherstellen ---
mc.recover_low(mypose)
print("\nRecovered lowest-energy pose.")
print(f"Final (lowest) score: {scorefxn(mypose):.3f}")

