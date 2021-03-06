#!/usr/bin/env python
# encoding: utf-8


import httplib

import urlparse

import doctest

def HttpExists(url):

    host, path = urlparse.urlsplit(url)[1:3]

    print "host = ", host, "path = ", path

    if ':' in host:

        # port specified, try to use it
        host, port = host.split(':', 1)

        try:

            port = int(port)

        except ValueError:

            print 'invalid port number %r' % (port,)

            return False

    else:

        # no port specified, use default port
        port = None

    try:

        connection = httplib.HTTPConnection(host, port = port)

        connection.request("HEAD", path)

        resp = connection.getresponse( )

        print "resp.status= ", resp.status

        if resp.status == 200:       # normal 'found' status

            found = True

        elif resp.status == 302:     # recurse on temporary redirect

            found = HttpExists(urlparse.urljoin(url,
                               resp.getheader('location', '')))

        else:                        # everything else -> not found

            print "Status %d %s : %s" % (resp.status, resp.reason, url)

            found = False

    except Exception, e:

        print e.__class__, e, url

        found = False


    return found


def _test( ):

    return doctest.testmod(HttpExists)


if __name__ == "__main__":

    #_test( )
    print HttpExists("blog.csdn.net")

    print HttpExists("http://blog.csdn.net")

    print HttpExists("http://blog.csdn.net/")

    print HttpExists("http://blog.csdn.net/gatieme")

    print HttpExists("http://blog.csdn.net/gatieme/article/list/1")
