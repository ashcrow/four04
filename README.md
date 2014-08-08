four04
======
404 Sensor for https://isc.sans.edu/404project/


Requirements
------------
* Python
* uwsgi
* Proxy server (nginx, apache, etc..)
* SANS API credentials


Configuration
-------------
Edit config.json and fill in the missing information. You can also add more
files in the ROUTES section where the object key is the URL path and the value
is an array of response code and file on the file system to return.

Example
~~~~~~~
```JSON
{
    "SANS_USERID": "00000000",
    "SANS_KEY": "123456789012345678901234567890",
    "IP_MASK": "0xffffffff",
    "ENDPOINT": "https://isc.sans.edu/weblogs/404project.html?id=%s&version=2",
    "ROUTES": {
        "": ["503 Service Unavailable", "pages/503.html"],
        "/test": ["200 OK", "pages/test.html"],
        "/some/special/location": ["200 OK", "pages/special.html"]
    }
}
```

Running
-------
To run the server execute: ```uwsgi uwsgi/uwsgi.ini```. If you want to
change any of the uwsgi application server configuration items edit
uwsgi/uwsgi.ini. By default it will listen on 127.0.0.1 port 8080.

**Note**: The default configuration will drop privledges to nobody.nobody.

Update your application server to pass everything (or a subset of things)
to 127.0.0.1:8080.

Nginx Example
~~~~~~~~~~~~~

```Nginx
location / {
    proxy_pass http://127.0.0.1:8080;
}
```

See Also
--------
* https://bitbucket.org/ashcrow/pysans404
