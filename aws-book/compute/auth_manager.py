from  boto.ec2 import connect_to_region
from compute.constants import ec2_avail_regions as REGIONS


class AwsAuth(object):

    def __init__(self):
        pass


    def get_ec2_conn(self, region):

        if region not in REGIONS:
            raise RegionError('Not appropriate region for EC2 service.')
        else:
            return connect_to_region(region)




class ConnectionObject(object):

    def __init__(self):
        self.__conns = {}
        self.conn_obj = AwsAuth()

    def get_conn(self, region):

        conn = self.__conns.get(region)

        if conn is None:
            conn = self.conn_obj.get_ec2_conn(region)
            self.__conns.update({region: conn})

        return conn