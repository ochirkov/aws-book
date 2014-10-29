# Standart libs
import os.path

# Custom packages
from auth_manager import ConnectionObject
from constants import ec2_avail_regions as REGIONS


class AWSCreds(ConnectionObject):

    def __init__(self, region=None):
        super(AWSCreds, self).__init__(region)
        self.conn = self.get_conn()


    def ssh_keys_list(self):

        keys = {}
        keys.update({self.region:[ i.name for i in self.conn.get_all_key_pairs() ]})
        return keys


    def create_keys(self, key_pair_name, save=False):
        try:
            key = self.conn.create_key_pair(key_pair_name)
            if save is True:
                key.save(os.path.join(os.path.expanduser('~'), '.ssh'))
            return key
        except Exception as e:
            return e


    def upload_key(self, key_pair_name, public_key_file):
        try:
            key = self.conn.import_key_pair(key_pair_name, public_key_file)
            return key
        except Exception as e:
            print e


    def cross_copy_key(self, key_pair_name):

        key = self.conn.get_key_pair(key_pair_name)
        current_region = self.conn.region.name

        try:
            for i in REGIONS:
                if i == current_region:
                    continue
                print i
                super(AWSCreds, self).__init__(i)
                conn = self.get_conn()
                key.copy_to_region(conn.region)
        except Exception as e:
            print e


    def get_key(self, key_pair_name):

        try:
            key = self.conn.get_key_pair(key_pair_name)
        except Exception as e:
            print e

        return key


    def remove_key(self, key_pair_name):

        key = self.get_key(key_pair_name)
        key.delete()
        return True