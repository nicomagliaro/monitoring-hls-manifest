import os
import datetime

class Housekeep:

    def __init__(self, path='/var/tmp/hls', retention=5):
        self.path = path
        self.retention = retention
        self._basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def remove_recurse(self, to_delete):
        """
        Function to recursively remove all files and directories in the given path
        :param str
        """
        dir_list = os.listdir(to_delete)
        for item in dir_list:
            if os.path.isdir(item):
                self.remove_recurse(item)
            elif os.path.isfile(item):
                os.remove(item)

    def delete_old(self):
        """
        Function to delete all old files / folders in the given path
        """
        path = os.path.abspath(self.path)
        now = datetime.datetime.now()
        dir_list = os.listdir(path)
        for directory in dir_list:
            if os.path.isdir(os.path.join(path, directory)):
                timestamp = os.path.getmtime(os.path.join(path, directory))
                st = datetime.datetime.fromtimestamp(timestamp)
                if now - st > datetime.timedelta(minutes=int(self.retention)):
                    os.chdir(os.path.join(path, directory))
                    self.remove_recurse(os.path.join(path, directory))
                    os.rmdir(os.path.join(path, directory))
                    os.chdir(self._basedir)
                else:
                    continue





