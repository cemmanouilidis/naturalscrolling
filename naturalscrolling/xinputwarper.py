import os
import re


class XinputWarper(object):
    # Singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(XinputWarper, cls).__new__(cls, *args,
                                                                 **kwargs)
            cls._instance.__xinput_list_pattern = re.compile(
                r'\s+([A-z0-9\s\-\(\)\/]+)\s+id=(\d+)\s+\[slave\s+pointer.*\]')
            cls._instance.__xinput_list = None
        return cls._instance

    def get_xinput_list(self):
        return self.__xinput_list
    xinput_list = property(get_xinput_list)

    def enable_natural_scrolling(self, devise_xid, enabled):
        """
        Global method to apply or not Natural Scrolling
        """
        map = os.popen("xinput get-button-map \"%s\"" %
                       devise_xid).read().strip()

        if enabled == True:
            map = map.replace("4 5", "5 4")
            map = map.replace("6 7", "7 6")
        else:
            map = map.replace("5 4", "4 5")
            map = map.replace("7 6", "6 7")

        os.system("xinput set-button-map \"%s\" %s" %(devise_xid, map))

    def find_xid_by_name(self, name):
        """
        Extract from the xinput list the id of the given device name
        """
        xinput_list = self._xinput_list(name)
        for device_info in self.__xinput_list_pattern.findall(xinput_list):
            if device_info[0].strip() == name:
                return device_info[1]
        return None

    def first_xid(self):
        """
        Extract from the xinput list the id of the first detected device
        """
        xinput_list = self._xinput_list()
        return self.__xinput_list_pattern.findall(xinput_list)[0][1]

    def reset_cache(self):
        """
        Clear xinput cache in order to force refresh
        """
        self.__xinput_list = None

    def _xinput_list(self, name=None):
        """
        Refresh cache and/or search in cached xinput list
        """
        if not self.__xinput_list:
            self.__xinput_list = os.popen(("xinput list | grep -v 'XTEST' "
                                           "| grep -v '\[master '")).read()

        if name:
            return re.search(r'(.*%s.*)' % re.escape(name),
                self.__xinput_list).group(1)
        else:
            return self.__xinput_list
