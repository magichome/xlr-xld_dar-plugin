#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
from xlddar.XLDeployClient import XLDeployClient

xldClient = XLDeployClient.create_client(xldeployServer, username, password)

xldClient.upload_package(ciDirectory, ciApplication, ciVersion, xmlDescriptor)