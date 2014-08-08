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
404 sensor for https://isc.sans.edu/404project/.
"""

import json
import uwsgi

__version__ = '0.1.0'

try:
    CONFIG = json.load(open('config.json', 'r'))
except Exception, ex:
    raise Exception('Could not parse config: %s' % ex)


def application(environ, start_response):
    """
    WSGI application to handle 404's.
    """
    # Remove wsgi.* items
    for key in environ.keys():
        if key.startswith('wsgi.'):
            del environ[key]

    # Pass data to the mule
    uwsgi.mule_msg(json.dumps(environ))

    # '' is the default route
    route_to = ''
    if environ['PATH_INFO'] in CONFIG['ROUTES'].keys():
        route_to = environ['PATH_INFO']

    status, html_file = map(str, CONFIG['ROUTES'][route_to])

    # Return data to the user
    start_response(status, [('Content-Type', 'text/html')])
    with open(html_file, 'r') as data:
        for line in data.readlines():
            yield line
