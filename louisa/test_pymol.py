from pyrosetta import *
from pyrosetta.rosetta import protocols

init(extra_options="-ignore_unrecognized_res")

# Erstelle eine kleine Pose
pose = pose_from_sequence("ACDE")

# ✅ PyMOLObserver jetzt ohne Argumente initialisieren
obs = protocols.moves.PyMOLObserver()

# ✅ zur Pose hinzufügen
obs.add_to(pose)

# ✅ erste Pose an PyMOL senden
obs.pymol().apply(pose)

print("✅ Verbindung erfolgreich! Sieh in PyMOL nach — sollte 'ACDE' zeigen.")

