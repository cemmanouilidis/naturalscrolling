import pyudev
from naturalscrolling_lib.udevobservator import UDevObservator
from naturalscrolling.xinputwarper import XinputWarper
from naturalscrolling_lib.gconfsettings import GConfSettings, GConfKey


class Debugger(object):

    def execute(self):
        print " * PyUDev\n"
        print "\tAll devices:\n\t============"
        for device in pyudev.Context().list_devices():
            if device.sys_name.startswith("event"):
                print "\t\t", device.sys_name, device.parent["NAME"][1:-1]

        print "\n\tInput devices:\n\t=============="
        for device in pyudev.Context().list_devices(subsystem="input"):
            if device.sys_name.startswith("event"):
                print "\t\t", device.sys_name, device.parent["NAME"][1:-1]

        print "\n\tID_INPUT_MOUSE and input devices:\n\t======================="
        for device in pyudev.Context().list_devices(subsystem="input",
                                                    ID_INPUT_MOUSE=True):
            if device.sys_name.startswith("event"):
                print "\t\t", device.sys_name, device.parent["NAME"][1:-1]


        print "\n\tID_INPUT_MOUSE devices:\n\t======================="
        for device in pyudev.Context().list_devices(ID_INPUT_MOUSE=True):
            if device.sys_name.startswith("event"):
                print "\t\t", device.sys_name, device.parent["NAME"][1:-1]

        print "\n\n * XinputWarper\n"
        print "\t- First XID: %s\n" % XinputWarper().first_xid()

        print "\t- Devices:\n\t=========="
        for device in UDevObservator().gather_devices():
            print "\t\tDevice \"%s\" has XID %s" % (device.values()[0],
                                                device.keys()[0])

        print "\n\t- Xinput list:\n\t=========="
        for xinput in XinputWarper().xinput_list.split("\n"):
            print "\t\t", xinput

        print "\n\n * GConfSettings\n"
        print "\t- All Keys:\n\t==========="
        for entry in GConfSettings().keys():
            gconf_key = GConfKey(entry.key, entry.value.type)
            print "\t\tKey \"%s\" has value \"%s\"" % (gconf_key.name,
                                                   gconf_key.get_value())
