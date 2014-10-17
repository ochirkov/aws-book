#!/usr/bin/python

import argparse
import os.path
import sys
import string


# Create parser object for access/secret keys args
#
parser = argparse.ArgumentParser()

parser.add_argument('-k', '--key', action='store', required=True, help='Access key ID')
parser.add_argument('-s', '--secret', action='store', required=True, help='Secret key')

values = vars(parser.parse_args())


# Create boto config template
#
boto_config_template = string.Template("""
[Credentials]
aws_access_key_id = $key
aws_secret_access_key = $secret
""")


# If boto config doesn't exist create one
#
boto_config_path = os.path.join(os.path.expanduser('~'), '.boto')

if os.path.exists(boto_config_path):
    print "This file already exists."
    sys.exit(1)
else:
    with open(boto_config_path, "w+") as f:
        f.write(boto_config_template.substitute(values))
