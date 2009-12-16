import json, os, subprocess
from optparse import OptionParser

ACTIONS = ['install', 'debug', 'package', 'deploy', 'log']


def parse_appinfo(dest_dir):
    """Reads the content of the appinfo file and
    decodes the json"""
    content = open(os.path.join(dest_dir, "appinfo.json")).read()
    appinfo = json.loads(content)
    return appinfo

def package(dest_dir):
    """ Packages the application"""
    ret_code = subprocess.call(["palm-package", dest_dir])
    if ret_code


def install(dest_dir, appinfo, version=None):
    """ Installs version number xxx to the device"""
    pass


def main_func():

    usage = """usage: %prog [options] action

Use PyPalm to control your development process on the webOS device.

    install - installs the current version of the app on the device
    package - package the current version
    deploy - package and deploy
    debug - start the debugger
    log - get log output from the device"""
    parser = OptionParser(usage)
    parser.add_option("-d", "--device", dest='device',
                      help="Target device: [tcp|usb]", default="tcp")
    
    (options, args) = parser.parse_args()
    
    # Get the action arg
    if len(args) == 0:
        parser.print_help()
        exit()

    if not args[0] in ACTIONS:
        parser.error("%s must be one of: %s" % (args[0], ", ".join(ACTIONS)))

    # We always assume this dir
    current_dir = os.getcwd()
    app_info = parse_appinfo(current_dir)

    if args[0] == "package":
        package(current_dir)
