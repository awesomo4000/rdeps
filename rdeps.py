#! /usr/bin/env python
"""
Usage: %s binary1 [ELF bin1] [ELF bin2] ...

List dependencies for ELF files

-r : Recursively find dependencies, searching RDEPS_PATH

ENVIRONMENT VARIABLES

RDEPS_PATH : colon-delimited directories to search (-r for recursive) for 
             dependencies of input files given on command line.

"""

import json
import os.path
import sys

from elftools.elf.elffile import ELFFile

def usage():
  sys.stdout.write(__doc__ % os.path.basename(sys.argv[0]))


def in_directory(filename, directory):
  # make both absolute
  directory = os.path.join(os.path.realpath(directory), '')
  filename  = os.path.realpath(filename)

  # return true, if the common prefix of both is equal 
  # to directory e.g. /a/b/c/d.rst and directory is /a/b, 
  # the common prefix is /a/b

  return os.path.commonprefix([filename, directory]) == directory


def undelimit(s, delimiter=':'):
  # return list of entries from string delimited by delimiter
  if not s: return []

  # Return unique list of string split on delimiter

  return filter(lambda x:any(x),
                list(set(s.split(delimiter))))


def deps(filename):
  # Return list of dependencies for file

  if not filename:
    return []

  if not os.path.isfile(filename):
    return []

  dlist = []

  with open(filename, 'rb') as f:
    try: 
      elf = ELFFile(f)
    except:
      return []

    for segment in elf.iter_segments():
      if segment.header['p_type'] == 'PT_DYNAMIC':
        for tag in segment.iter_tags(type='DT_NEEDED'):
          dlist.append(tag.needed)

    return list(set(dlist))

def find_file(filename, pathlist):
  #
  # find the first available file in pathlist matching filename
  #

  if os.path.exists(filename):
    return os.path.realpath(filename)
  
  file_list = []
  for path in pathlist:
    for root, dirs, files in os.walk(path, topdown=False):
      if filename in files:
        return os.path.join(root, filename) # XXX:only returns first one
  return None

def recurse_deps(filename, pathlist, dep_dict = {} ):

  path_dict = dep_dict.setdefault( filename,
              { 'path' : find_file(filename, pathlist ) })

  for f in deps(path_dict['path']):
    curr_deps  = dep_dict[filename].setdefault('deps',[])
    if f in curr_deps:
      continue
    curr_deps += [f] 
    recurse_deps(f, pathlist, dep_dict)
  return dep_dict

#-----------------------------------------------------------

if __name__ == "__main__":

  if len(sys.argv) < 2:
    usage()
    sys.exit(0)

  DO_RECURSIVE = False

  if '-r' in sys.argv[1:]:
    DO_RECURSIVE = True

  filelist = set(filter(lambda x: x != '-r', sys.argv[1:]))

  for f in filelist:
    if DO_RECURSIVE:
      rpaths    = undelimit(os.environ.get("RDEPS_PATH")) 
      deps_dict = recurse_deps(f, rpaths)
      print json.dumps(deps_dict, indent=2, sort_keys=True)
    else:
      for d in deps(f):
        print f,d
