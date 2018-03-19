#! /usr/bin/env python
"""
Usage: %s [-j] [-r] [ELF bin1] [ELF bin2] ...

List dependencies for ELF files

-r : Recursively find dependencies, searching RDEPS_PATH
-j : Output JSON

ENVIRONMENT VARIABLES

RDEPS_PATH : colon-delimited directories to search (-r for recursive) for 
             dependencies of input files given on command line.

"""

import json
import os.path
import sys

from elftools.elf.elffile import ELFFile

try:  # py3
  from shlex import quote
except ImportError:  # py2
  from pipes import quote

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

def get_dependencies(filename, pathlist=[], dep_dict = {}, recurse=False):

  path_dict = dep_dict.setdefault( filename,
              { 'path' : find_file(filename, pathlist ) })

  for f in deps(path_dict['path']):
    curr_deps  = dep_dict[filename].setdefault('deps',[])

    if f in curr_deps: continue

    curr_deps += [f] 

    if recurse:
      get_dependencies(f, pathlist, dep_dict, recurse=True)
    else:
      dep_dict.setdefault(f, {'path' : find_file(f, pathlist),
                              'deps' : [] } )

  return dep_dict

def rm_opts(opt):
  return opt not in ( '-r', '-j' )

#-----------------------------------------------------------------------------

if __name__ == "__main__":

  if len(sys.argv) < 2:
    usage()
    sys.exit(0)

  opt_recurse, opt_json = False, False

  if '-r' in sys.argv[1:]: opt_recurse = True
  if '-j' in sys.argv[1:]: opt_json = True

  filelist = set(filter(rm_opts, sys.argv[1:]))

  pathlist = undelimit(os.environ.get("RDEPS_PATH"))

  dep_dict = {} 

  for filename in filelist:
    dep_dict = get_dependencies(filename, pathlist, dep_dict,
                                recurse=opt_recurse)

  if opt_json:
    sys.stdout.write(json.dumps(dep_dict, indent=2, sort_keys=True))

  else:
    for k,v in dep_dict.items():
      out = quote(k)
      if v['path']:
        out += ',' + quote(v['path'])
      out += '\n'
      sys.stdout.write(out)
