import json, os, subprocess, re
import StringIO

from optparse import OptionParser

ACTIONS = ['install', 'debug', 'package', 'deploy', 'log',
           'emulator', 'clean', 'start', 'remove']
QUIET = True


def is_app_dir(dest_dir):
    return os.path.exists(os.path.join(dest_dir, "appinfo.json"))


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

def main_func():

    usage = """usage: %prog [options] action

Use PyPalm to control your development process on the webOS device.

    install - installs the current version of the app on the device
    package - package the current version
    deploy - package and deploy
    debug - start the debugger
    log - get log output from the device
    clean - remove old IPK files
    remove - Uninstall the application
    start - Start the application
    emulator - start the emulator """

    
    parser = OptionParser(usage)
    parser.add_option("-d", "--device", dest='device',
                      help="Target device: [tcp|usb]", default="tcp")
    parser.add_option("-i", "--version", dest="version",
                      help="Version to install", default=None)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      help="Print verbose output")
    
    (options, args) = parser.parse_args()
    
    # Get the action arg
    if len(args) == 0:
        parser.print_help()
        exit()

    # If this is not an app dir exit
    if not is_app_dir(os.getcwd()):
        print "This is not a Palm webOS application directory!"
        exit()


    # Check for the output
    if options.verbose:
        QUIET = False
    else:
        QUIET = True


    if not args[0] in ACTIONS:
        parser.error("%s must be one of: %s" % (args[0], ", ".join(ACTIONS)))

    # We always assume this dir
    current_dir = os.getcwd()
    app_info = parse_appinfo(current_dir)

    if args[0] == "package":
        package(current_dir, app_info, quiet=QUIET)
    elif args[0] == "install":
        install(current_dir, app_info, version=options.version,
                device=options.device, quiet=QUIET)
    elif args[0] == 'emulator':
        emulator()
    elif args[0] == 'log':
        log(app_info, device=options.device)
    elif args[0] == "deploy":
        package(current_dir, app_info, quiet=QUIET)
        install(current_dir, app_info, version=options.version,
                device=options.device, quiet=QUIET)
    elif args[0] == "debug":
        debug(app_info)
    elif args[0] == 'clean':
        clean(current_dir, app_info)
    elif args[0] == 'start':
        start(current_dir, app_info['id'], device=options.device)
    elif args[0] == 'remove':
        remove(current_dir, app_info['id'], device=options.device, quiet=QUIET)
