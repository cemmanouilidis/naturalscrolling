import pyudev
from naturalscrolling_lib.udevobservator import UDevObservator
from naturalscrolling.xinputwarper import XinputWarper
from naturalscrolling_lib.gconfsettings import GConfSettings, GConfKey


class Debugger(object):

    def execute(self):
        print " * PyUDev\n"
        print "\n\tInput devices:\n\t=============="
        devices = pyudev.Context().list_devices(subsystem="input")
        for device in devices:
            if device.sys_name.startswith("event"):
                print "\t\t", device.sys_name, device.parent["NAME"][1:-1]

        print "\n\tInput devices keys:\n\t=============="
        for device in devices:
            device_keys = ""
            if device.sys_name.startswith("event"):
                if device.parent.keys():
                    for key in device.parent.keys():
                        device_keys += "{%s: %s}," % (key, device.parent[key])
                    print "%s => %s" % (device.sys_name, device_keys)

        print "\n\n * XinputWarper\n"
        print "\t- First XID: %s\n" % XinputWarper().first_xid()

        print "\t- Devices:\n\t=========="
        devices = UDevObservator().gather_devices()
        print "\n\t%d device(s) found\n" % len(devices)
        for device in devices:
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
