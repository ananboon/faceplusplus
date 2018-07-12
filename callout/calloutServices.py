
import urllib
import urllib2
import json
import time
from utilities.log import Log

# [Callout_Service]


# def callout_post_message(url, payload):
#
#     Log.debug('server url :' + url)
#     Log.debug('payload :' + json.dumps(payload))
#
#     data = urllib.urlencode(payload)
#     try:
#         req = urllib2.Request(url, data)
#         response = urllib2.urlopen(req)
#         response.read()
#     except urllib2.HTTPError as e:
#         Log.fatal(e.message)
#     return None


def callout_post(req):
    try:
        # post data to server
        resp = urllib2.urlopen(req, timeout=5)
        # get response
        qrcont=resp.read()
        return qrcont
    except urllib2.HTTPError as e:
        Log.fatal(e.read())
    return None


def create_request(http_url, **payload):
    Log.info('url : '+http_url)
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for (k, v) in payload.iteritems():
        Log.debug('key :' + k)
        Log.debug('value :' + v)
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
        data.append(v)
    data.append('--%s--\r\n' % boundary)
    http_body = '\r\n'.join(data)
    Log.info(http_body)
    # buld http request
    req = urllib2.Request(http_url)
    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    req.add_data(http_body)
    return req
