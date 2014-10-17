# Custom packages
from compute.auth_manager import AwsAuth


class AWSSecGroups(object):

    def __init__(self, region=None):
        self.region = region
        self.conns = AwsAuth().conns


    def sec_groups_list(self):

        sec_groups = {}

        for region in self.conns:
            conn = self.conns[region]
            sec_groups.update({region:[ i.name for i in conn.get_all_security_groups() ]})

        return sec_groups


    def create_sec_group(self, sec_group_name, description, vpc=None):
        try:
            conn = self.conns[self.region]
            sec_group = conn.create_security_group(sec_group_name, description, vpc_id=vpc)
            return sec_group
        except Exception as e:
            return e


    def manage_sec_rules(self,
                          name,
                          ip_protocol,
                          from_port,
                          to_port,
                          cidr_ip,
                          flag=None):

        conn = self.conns[self.region]

        try:
            for i in conn.get_all_security_groups():
                if i.name == name:
                    sec_group = i

                    if flag not in ('authorize', 'revoke'):
                        print "Use authorize or revoke as flag option"
                    else:
                        getattr(sec_group, flag)(ip_protocol=ip_protocol,
                                                 from_port=from_port,
                                                 to_port=to_port,
                                                 cidr_ip=cidr_ip)
                        return True
        except Exception as e:
            return e


    def get_sec_group(self, name):

        conn = self.conns[self.region]
        for i in conn.get_all_security_groups():
            if i.name == name:
                return i


    def remove_sec_group(self, name):

        sec_group = self.get_sec_group(name)
        sec_group.delete()
        return True