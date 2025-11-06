from pyrosetta import *
from pyrosetta.rosetta.protocols.rosetta_scripts import XmlObjects
from register_mover import register

# 🔹 1. Registriere deinen Mover-Creator
register()

# 🔹 2. Starte PyRosetta
pyrosetta.init()

# 🔹 3. Lies Pose ein (hier z. B. testweise eine Ala5-Kette)
pose = pose_from_pdb("/home/louisa_menges/pdbs/1UBQ.pdb")

from pyrosetta.rosetta.protocols.moves import MoverFactory
print(MoverFactory.get_instance().mover_exists("BootcampMover"))

# 🔹 4. Definiere XML
EMBEDDED_XML = """<ROSETTASCRIPTS>
  <SCOREFXNS>
    <ScoreFunction name="sfxn" weights="ref2015"/>
  </SCOREFXNS>
  <MOVERS>
    <BootcampMover name="bootcamp"
                     num_iterations="50"
                     min_phi="-10" max_phi="10"
                     min_psi="-10" max_psi="10"
                     scorefxn="sfxn"/>
  </MOVERS>
  <PROTOCOLS>
    <Add mover_name="bootcamp"/>
  </PROTOCOLS>
</ROSETTASCRIPTS>
"""

# 🔹 5. Erzeuge das Protokoll aus XML
xmlobj = XmlObjects.create_from_string(EMBEDDED_XML)
protocol = xmlobj.get_mover("ParsedProtocol")

# 🔹 6. Führe das Protokoll aus
protocol.apply(pose)

# 🔹 7. Speichere Ergebnis
pose.dump_pdb("output.pdb")

print("✅ BootCampMover run complete — results in output.pdb")


