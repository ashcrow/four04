# Copyright (c) 2014, Steve Milner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
# * Neither the name of the organization nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
Worker process (mule) which pushes data to the endpoint.
"""

import base64
import datetime
import socket
import struct
import urllib

import uwsgi
import json


try:
    CONFIG = json.load(open('config.json', 'r'))
except Exception, ex:
    raise Exception('Could not parse config: %s' % ex)


def apply_mask_to_ip(ip):
    """
    Applies mask to the ip.
    """
    packed = socket.inet_aton(ip)
    lng = struct.unpack("!L", packed)[0] & int(CONFIG['IP_MASK'], 16)
    return socket.inet_ntoa(struct.pack('!L', lng))


def loop():
    """
    Main mule loop. As messages come in data is sent to the endpoint.
    """
    while True:
        environ = json.loads(uwsgi.mule_get_msg())

        uri = environ['PATH_INFO']
        remote_addr = apply_mask_to_ip(environ['REMOTE_ADDR'])
        user_agent = environ['HTTP_USER_AGENT']

        dt = datetime.datetime.now()

        # Use \0 as a delimiter.
        data = "\0".join([
            CONFIG['SANS_USERID'], CONFIG['SANS_KEY'], uri,
            remote_addr, user_agent,
            dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M:%S'),
            CONFIG['IP_MASK']])
        try:
            result = urllib.urlopen(
                CONFIG['ENDPOINT'] % urllib.quote(CONFIG['SANS_USERID']),
                urllib.urlencode({'DATA': base64.encodestring(data)}))
            if int(result.getcode()) != 200:
                raise Exception('Did not get a 200')
        except Exception, ex:
            raise Exception('Could not send data: %s' % ex)


if __name__ == '__main__':
    loop()
