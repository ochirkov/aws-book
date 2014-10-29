from  boto.ec2 import connect_to_region


class AwsAuth(object):

    """
    Help on class AwsAuth in auth_manager module:

    NAME
        AwsAuth

    DESCRIPTION
        This class provides an method for getting connection object
        to specified region.

    METHODS

        __init__(self)
            Does nothing.

        get_ec2_conn(self, region)
            Create connection object with specified region.

            :return: The newly created connection to the EC2 region.

    """

    def __init__(self):
        pass


    def get_ec2_conn(self, region):

        return connect_to_region(region)



class ConnectionObject(object):

    """
        Help on class ConnectionObject in auth_manager module:

    NAME
        ConnectionObject

    DESCRIPTION
        This class provides an object of AwsAuth class.
        self.__conns attribute stores already initialized connection objects.
        If requested connection object doesn't exist in self.__conns get_conn method
        will get it from get_ec2_conn method of AwsAuth class and store it to self.__conns.
        Other classes should inherit this class for quick access to the connection objects.

    METHODS

        __init__(self, region)
            Init method initialize self.__conns dictionary for connection objects storing.
            It also create AwsAuth class instance and initialize requested region attribute.

        get_conn(self)
            Tries grab connection object from self.__conns attribute. If there is no such
            object method tries calls this object from get_ec2_conn method from AwsAuth class.

            :return: connection to the EC2 region by requested region.
    """

    def __init__(self, region):
        self.__conns = {}
        self.conn_obj = AwsAuth()
        self.region = region


    def get_conn(self):

        conn = self.__conns.get(self.region)

        if conn is None:
            conn = self.conn_obj.get_ec2_conn(self.region)
            self.__conns.update({self.region: conn})

        return conn