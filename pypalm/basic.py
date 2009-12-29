import json, os, subprocess, re
import StringIO


def call_and_return(args):
    p = subprocess.Popen(args, stdout = subprocess.PIPE)
    out = p.communicate()[0]
    # Return the tuple of code and content
    return (p.returncode, out)

def parse_appinfo(dest_dir):
    """Reads the content of the appinfo file and
    decodes the json"""
    content = open(os.path.join(dest_dir, "appinfo.json")).read()
    appinfo = json.loads(content)
    return appinfo

def package(dest_dir, appinfo, quiet=True):
    """ Packages the application"""
    (ret_code, output) = call_and_return(["palm-package", dest_dir])
    
    if ret_code < 0:
        print "package was called and terminted with a failure code"

    if not quiet:
        print output

    print "Packaged application with version %s" % appinfo["version"]
        
def install(dest_dir, appinfo, version=None, device="tcp", quiet=True):
    """ Installs version number xxx to the device"""
    if not version:
        version = appinfo["version"]

    filename = appinfo["id"] + "_" + version + "_all.ipk"
    if os.path.exists(os.path.join(dest_dir, filename)):
        # Call the install process
        args = ["palm-install"]

        # add the device
        args.append("-d")
        args.append(device)

        # Add the version
        args.append(filename)
        
        (ret_code, output) = call_and_return(args)
        if ret_code < 0:
            print "Could not install application %s" % appinfo["id"]

        if not quiet:
            print output

        print "Installed application with version %s" % version
        
    else:
        print "could not find packaged file for version %s" % version


def emulator():
    """ Start the emulator """
    call_and_return("palm-emulator")

def debug(appinfo):
    """Start the debugger """
    # Directly start novaterm in the beginning
    os.execl("/usr/bin/novaterm")

def log(appinfo, device="tcp"):
    """ Print the log output """
    args = ["palm-log"]

    # Set the device
    args.append("-d")
    args.append(device)

    # Set the appid
    args.append(appinfo["id"])

    (ret_code, output) = call_and_return(args)
    print output

def clean(dest_dir, appinfo):
    """ Clear IPK files"""
    m = re.compile("%s.*\.ipk$" % appinfo["id"].replace(".", "\\."))
    for f in os.listdir(dest_dir):
        if m.search(f):
            os.remove(f)


def start(dest_dir, id, device='tcp'):
    """ Lauch the app"""
    args = ['palm-launch']
    
    args.append('-d')
    args.append(device)

    args.append(id)

    (ret_code, output) = call_and_return(args)
    if ret_code < 0:
        print output
        print "There was an error"

def remove(dest_dir, id, device='tcp', quiet=True):
    args = ['palm-install']

    args.append('-d')
    args.append(device)

    args.append('-r')

    args.append(id)
    (ret_code, output) = call_and_return(args)
    if ret_code < 0:
        print output
        print "Could not remove the application"


    if not quiet:
        print output
