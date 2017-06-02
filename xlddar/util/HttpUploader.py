import base64, httplib, urllib

class HttpUploader(object):
    def __init__(self, http_connection, username, password):
        #  {proxyPort: None, password: xldadmin, title: XLD-dev, proxyHost: None, url: http://hlbldplyd001:4516/, username: admin}
        host = http_connection['url'].replace('http://', '').replace('https://', '')
        if host.endswith('/'):
            host = host[:-1];

        self.host = host
        self.username = http_connection['username']
        self.password = http_connection['password']

    def upload(self, selector, fields, files):
        content_type, body = HttpUploader.encode_multipart_formdata(fields, files)

        h = httplib.HTTPConnection(self.host)

        headers = {
            'User-Agent': 'XLRELEASE',
            'Authorization': 'Basic %s' % base64.b64encode(self.username+":"+self.password),
            'Accept-Encoding': 'multipart/form-data',
            'Content-Type': content_type,
            'Content-Length': str(len(body))
        }

        h.request('POST', selector, body, headers)

        resp = h.getresponse()

        if resp.status >= 400:
            raise Exception('[%s] %s - %s' % (resp.status, resp.reason, resp.read()))

    @staticmethod
    def encode_multipart_formdata(fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'

        buf = ''
        for (key, value) in fields:
            buf += '--%s\r\n' % BOUNDARY
            buf += 'Content-Disposition: form-data; name="%s"\r\n' % key
            buf += '\r\n' + value + '\r\n'

        for (key, filename, value) in files:
            buf += '--%s\r\n' % BOUNDARY
            buf += 'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename)
            buf += 'Content-Type: application/octet-stream\r\n'
            buf += '\r\n' + urllib.quote_plus(value) + '\r\n'
            buf += '--%s--\r\n\r\n' % BOUNDARY

        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY

        return content_type, buf
