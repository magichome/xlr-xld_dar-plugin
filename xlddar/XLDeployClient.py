#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, time, ast, re, base64, httplib, urllib2

from xlddar.util.InMemoryZip import InMemoryZip
from xlddar.util.HttpUploader import HttpUploader
from xlddar.poster.encode import multipart_encode, MultipartParam
from xlddar.poster.streaminghttp import register_openers

from xlrelease.HttpRequest import HttpRequest

class XLDeployClient(object):
    def __init__(self, http_connection, username=None, password=None):
        self.http_request = HttpRequest(http_connection, username, password)
        self.http_uploader = HttpUploader(http_connection, username, password)
        self.url = http_connection['url']
        if self.url.endswith('/'):
            self.url = self.url[:-1];
        self.username = http_connection['username']
        self.password = http_connection['password']

    @staticmethod
    def create_client(http_connection, username=None, password=None):
        return XLDeployClient(http_connection, username, password)

    def create_directory(self, ciId):
        createTask = "/deployit/repository/ci/%s" % ciId
        xml = '<core.Directory id="' + ciId + '" />'
        self.http_request.post(createTask, xml, contentType='application/xml')

    def create_application(self, ciId):
        createTask = "/deployit/repository/ci/%s" % ciId
        xml = '<udm.Application id="' + ciId + '" />'
        self.http_request.post(createTask, xml, contentType='application/xml')

    def upload_package(self, ciDirectory, ciApplication, ciVersion, xmlDescriptor):
        ciAppPath = ciApplication
        if len(ciDirectory) > 0:
            ciAppPath = ciDirectory + '/' + ciApplication

        xml = '<?xml version="1.0" encoding="UTF-8"?><udm.DeploymentPackage application="%s" version="%s">%s</udm.DeploymentPackage>' % (ciAppPath, ciVersion, xmlDescriptor)

        # create DAR in memory
        zipfile_ob = InMemoryZip()
        zipfile_ob.append("deployit-manifest.xml", xml)
        zipfile_ob.close()

        # prepare upload
        darname = ciApplication+'-'+ciVersion+'.dar'

        # write to tmp for upload
        filename = '/tmp/%s' % darname
        zipfile_ob.writetofile(filename)

        register_openers()

        mp = MultipartParam.from_file('fileData', filename)
        datagen, headers = multipart_encode([mp])

        # create request object
        request = urllib2.Request(self.url+'/deployit/package/upload/'+darname, datagen, headers)

        base64string = base64.b64encode('%s:%s' % (self.username, self.password))
        request.add_header("Authorization", "Basic %s" % base64string)

        # make request and return result
        print(urllib2.urlopen(request).read())
