# rdeps

Find dependencies in ELF objects, recursively if requested.

Simple output in normal mode, JSON output in recursive mode.

### Usage:
```
Usage: rdeps.py [-r] binary1 [ELF bin1] [ELF bin2] ...

List dependencies for ELF files

-r : Recursively find dependencies, searching RDEPS_PATH

ENVIRONMENT VARIABLES

RDEPS_PATH : colon-delimited directories to search (-r for recursive) for
             dependencies of input files given on command line.
```
### Examples

#### Without -r 
```sh
$ ./rdeps.py /bin/ls
/bin/ls libselinux.so.1
/bin/ls libacl.so.1
/bin/ls libc.so.6
```

#### With -r (recurse) option

Search ':' delimited paths in environment variable `RDEPS_PATH` for absolute paths of dependencies, recursively do this for each dependency until are found. *Note*: no check for cycles is made, so this could run forever. Let your patience be your guide.

```sh
$ RDEPS_PATH=/lib:/usr/lib:/sbin/lib ./rdeps.py -r /bin/ls
{
  "/bin/ls": {
    "deps": [
      "libselinux.so.1",
      "libacl.so.1",
      "libc.so.6"
    ],
    "path": "/bin/ls"
  },
  "ld-linux-x86-64.so.2": {
    "path": "/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2"
  },
  "libacl.so.1": {
    "deps": [
      "libattr.so.1",
      "libc.so.6"
    ],
    "path": "/lib/x86_64-linux-gnu/libacl.so.1"
  },
  "libattr.so.1": {
    "deps": [
      "libc.so.6"
    ],
    "path": "/lib/x86_64-linux-gnu/libattr.so.1"
  },
  "libc.so.6": {
    "deps": [
      "ld-linux-x86-64.so.2"
    ],
    "path": "/lib/x86_64-linux-gnu/libc.so.6"
  },
  "libdl.so.2": {
    "deps": [
      "ld-linux-x86-64.so.2",
      "libc.so.6"
    ],
    "path": "/lib/x86_64-linux-gnu/libdl.so.2"
  },
  "libpcre.so.3": {
    "deps": [
      "libc.so.6"
    ],
    "path": "/lib/x86_64-linux-gnu/libpcre.so.3"
  },
  "libselinux.so.1": {
    "deps": [
      "libdl.so.2",
      "libc.so.6",
      "libpcre.so.3",
      "ld-linux-x86-64.so.2"
    ],
    "path": "/lib/x86_64-linux-gnu/libselinux.so.1"
  }
}
```
