from pyrosetta.rosetta import protocols
from bootcamp_mover import BootcampMover

class BootcampMoverCreator(protocols.moves.MoverCreator):
    instances_ = list()

    def __init__(self):
        protocols.moves.MoverCreator.__init__(self)

    def create_mover(self):
        mover = BootcampMover()
        self.instances_.append(mover)
        return mover

    def keyname(self):
        return BootcampMover.mover_name()

    def provide_xml_schema(self, xsd):
        print("creator provide_xml_schema is called")
        BootcampMover.provide_xml_schema(xsd)
 
#global var
_py_mover_creators_ = []

def register():
    factory = protocols.moves.MoverFactory.get_instance()
    creator = BootcampMoverCreator()
    factory.factory_register(creator)
    _py_mover_creators_.append(creator)
