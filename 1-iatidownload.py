#!/usr/bin/env python

import sys
import ckan
import ckanclient
import urllib
from datetime import date
import os

def run(directory):
    url = 'http://iatiregistry.org/api'
    registry = ckanclient.CkanClient(base_location=url)
    for pkg_name in registry.package_register_get():
            pkg = registry.package_entity_get(pkg_name)
            for resource in pkg.get('resources', []):
                print resource.get('url')
                try:
                    save_file(pkg_name, resource.get('url'), dir)
                except Exception, e:
                    print "Failed:", e

def save_file(pkg_name, url, dir):
	webFile = urllib.urlopen(url)
	localFile = open(dir + '/' + pkg_name + '.xml', 'w')
	localFile.write(webFile.read())
	webFile.close()

if __name__ == '__main__':
    dir = 'packages/' + str(date.today())
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except Exception, e:
            print "Failed:", e
            print "Couldn't create directory"
    run(dir)
