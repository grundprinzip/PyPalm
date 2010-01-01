# -*- coding: utf-8 -*-

import os, re
import codecs
import json

def get_files(current_dir):
    files = []
    for root, dirs, fs in os.walk(current_dir):
        if ".git" in dirs:
            dirs.remove(".git")
        if ".svn" in dirs:
            dirs.remove(".svn")
        if "CVS" in dirs:
            dirs.remove("CVS")


        # Get all JS files
        for f in fs:
            if os.path.splitext(f)[1] == ".js":
                files.append(os.path.join(root, f))

    return files


def process_files(files):
    lexicon = {}
    exp = re.compile("\\$L\\(\"(.*?)\"(,.*)?\\)", re.M)
    
    for f in files:
        fid = codecs.open(f, "r", "utf-8")

        # Read the complete file
        fid.seek(0)
        data = fid.read()
        
        # Now find all occurrences
        for matches in exp.findall(data):
            if not matches[0].strip() in lexicon.keys():
                lexicon[matches[0].strip()] = u""

    return lexicon


def format_content(lexicon):
    kk = lexicon.keys().sort()

    res = "{\n"
    for e in kk:
        res += "\"%s\"\t:\t\"\",\n" % e
    res += "}\n"
    

def read_lang(lang_file):
    if not os.path.exists(lang_file):
        return {}
        
    fid = codecs.open(lang_file, "r", "utf-8")
    lang_data = json.load(fid)
    return lang_data


def merge_data(old_lang, new_lang):
    """Old lang values have precedence over new lange values, while new_lang has the keys"""
    import copy
    
    result = {}

    cpy = copy.copy(new_lang)
    
    for k,v in old_lang.iteritems():
        
        if k in new_lang:
            result[k] = v
        else:
            result[k] = ""
            
        del cpy[k]

    for k,v in cpy.iteritems():
        result[k] = v

    return result

def supported_langs(current_dir):
    """Retrieves the supported langauges from the framework_configs"""
    
    if not os.path.exists(os.path.join(current_dir, "framework_config.json")):
        return []
    
    framework_config = json.load(open(os.path.join(current_dir, "framework_config.json")))
    
    # Check for langs array
    if framework_config.has_key("languages"):
        return framework_config["languages"]


def create_language_directories(current_dir, lang):
    """ Create the required directories if necessary"""
    if not os.path.exists(os.path.join(current_dir, "resources")):
        os.mkdir(os.path.join(current_dir, "resources"))

    if not os.path.exists(os.path.join(current_dir, "resources", lang)):
        os.makedirs(os.path.join(current_dir, "resources", lang))

def save_language(current_dir, lang, data):
    """ Save the language data to the JSON file """
    fid = open(os.path.join(current_dir, "resources", lang, "strings.json"), "w")
    json.dump(data, fid, sort_keys=True, indent=4)
    fid.close()


def localize(current_dir, quiet=True):
    """ This is the main function called from the module to
    localize the application"""

    # First check which languages we should support
    languages = supported_langs(current_dir)

    # Now get all source files
    files = get_files(current_dir)

    # get all language data
    lexicon = process_files(files)

    # For all supported langauges we need
    # to read the contents merge the contents and write them again
    for l in languages:

        l_data = read_lang(os.path.join(current_dir, "resources", l, "strings.json"))
        merged = merge_data(l_data, lexicon)

        # Create dirs
        create_language_directories(current_dir, l)

        # Write the languages
        save_language(current_dir, l, merged)
        print "Updated %s" % l
