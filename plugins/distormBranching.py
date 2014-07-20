from ODA.documentation.pluginprototype import PlugInTemplate
#Feed this an blob of assembly as a binary string
class Code:
    def __init__(self):
        pass
    def on_branch(self, offset, branch_type):
        pass
    def first_pass(self):
        #Stop on every branch type to learn basic blocks
        pass
    def second_pass(self):
        #Stop on return to learn probably legit code
        pass
    def third_pass(self):
        #Function signatures
        pass
    def last_pass(self):
        #Straight linear disassembly
        pass

class BasicBlock:
    def __init__(self):
        pass

class PlugIn(PlugInTemplate):
    def __init__(self, app):
        super().__init__(app)