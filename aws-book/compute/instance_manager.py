# Custom packages
from boto.ec2.networkinterface import NetworkInterfaceSpecification
from boto.ec2.networkinterface import NetworkInterfaceCollection

from compute.auth_manager import AwsAuth


class EC2Worker(object):

    def __init__(self, region=None):
        self.region = region
        self.conns = AwsAuth().conns


    def create_instance(self,
                        ami,
                        key_name=None,
                        instance_type=None,
                        interfaces=None):

        conn = self.conns[self.region]
        try:
            node = conn.run_instances(ami,
                                      key_name=key_name,
                                      instance_type=instance_type,
                                      network_interfaces=interfaces)
            return node
        except Exception as e:
            print e


    def create_iface(self,
                     subnet_id=None,
                     groups=None,
                     pub_ip_flag=None):

        interface = NetworkInterfaceSpecification(subnet_id=subnet_id,
                                                  groups=groups,
                                                  associate_public_ip_address=pub_ip_flag)
        interfaces = NetworkInterfaceCollection(interface)
        return interfaces