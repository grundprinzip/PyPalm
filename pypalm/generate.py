import basic

def new_scene(dest_dir, name, quiet = True):
    """Create a new scene in the app directory"""
    args = ['palm-generate']
    # now the template
    args.append('-t')
    args.append('new_scene')
    args.append('-p')
    args.append("name=%s"% name)

    args.append(dest_dir)

    print " ".join(args)

    (code, output) = basic.call_and_return(args)
    if code < 0:
        print "Could not create new scene"
        print output
    elif not quiet:
        print output

    print "Generated scene %s in %s" % (name, dest_dir)
