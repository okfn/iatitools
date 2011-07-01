import sys
import ckan    
import urllib

def run():
    url = 'http://iatiregistry.org/api'
    import ckanclient
    registry = ckanclient.CkanClient(base_location=url)
    startnow = False
    for pkg_name in registry.package_register_get():
            pkg = registry.package_entity_get(pkg_name)
            for resource in pkg.get('resources', []):
                print resource.get('url')
                try:
                    save_file(pkg_name, resource.get('url'))
                except Exception, e:
                    print "Failed:", e
                    print "Did you create the /packages directory in the same folder as you're running this script?"

def save_file(pkg_name, url):
	webFile = urllib.urlopen(url)
	localFile = open('packages/' + url.split('/')[-1] + '.xml', 'w')
	localFile.write(webFile.read())
	webFile.close()

if __name__ == '__main__':
    import sys
    thetransactions = []
    run()
    

