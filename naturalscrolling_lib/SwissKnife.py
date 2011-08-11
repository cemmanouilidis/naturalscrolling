import os

class XinputReader (object):
    def get_slave_pointer (self, xinput_list_output):
        slavepointer = []
        for line in xinput_list_output.split('\n'):

            if 'id=' in line and 'pointer' in line and 'slave' in line and 'XTEST' not in line:
                id = line.split ('id=')[1].split()[0]
                slavepointer.append(id)
        
        return slavepointer


class XinputCommand (object):
    def list (self):
        return os.popen ('xinput list').read()


class SwissKnife (object):
    xinputreader  = None 
    xinputcommand = None

    @staticmethod
    def XinputReader():
        if SwissKnife.xinputreader is None:
            SwissKnife.xinputreader = XinputReader()

        return  SwissKnife.xinputreader


    @staticmethod
    def Xinput():
        if SwissKnife.xinputcommand is None:
            SwissKnife.xinputcommand = XinputCommand()

        return SwissKnife.xinputcommand

