# Standart libs
import os.path

# Custom packages
from compute.auth_manager import ConnectionObject
from compute.constants import ec2_avail_regions as REGIONS


class AWSCreds(ConnectionObject):

    def __init__(self, region=None):
        super(AWSCreds, self).__init__()
        self.region = region


    def ssh_keys_list(self):

        keys = {}self._ConnectionObject__conns:

        for region in REGIONS:

            conn = get_conn(region)
            keys.update({region:[ i.name for i in conn.get_all_key_pairs() ]})

        return keys


    def create_key(self,key_pair_name, save=False):
        try:
            conn = self.conns[self.region]
            key = conn.create_key_pair(key_pair_name)

            if save is True:
                key.save(os.path.join(os.path.expanduser('~'), '.ssh'))
            return key

        except Exception as e:
            return e


    def upload_key(self, key_pair_name, public_key_file):

        conn = self.conns[self.region]

        try:
            key = conn.import_key_pair(key_pair_name, public_key_file)
            print "%s key was created successfully for %s region" % (key_pair_name, conn.region.name)
            return key
        except Exception as e:
            print e


    def cross_copy_key(self, key_pair_name):

        conn = self.conns[self.region]

        try:
            key = conn.get_key_pair(key_pair_name)
        except Exception as e:
            print e

        for region in self.conns:
            try:
                key.copy_to_region(self.conns[region].region)
            except Exception as e:
                print e


    def get_key(self, key_pair_name):

        conn = self.conns[self.region]

        try:
            key = conn.get_key_pair(key_pair_name)
        except Exception as e:
            print e

        return key


    def remove_key(self, key_pair_name):

        key = self.get_key(key_pair_name)
        key.delete()
        return True




boto.ec2.connect_to_region("us-west-1",
                           aws_access_key_id=key,
                           aws_secret_access_key=secret)