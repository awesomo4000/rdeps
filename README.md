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

```sh
$ ./rdeps.py /bin/ls
/bin/ls,/bin/ls
libselinux.so.1
libacl.so.1
libc.so.6
```

```sh
$ ./rdeps.py /bin/ls /bin/cat /usr/bin/strings /usr/lib/libbfd-2.24-system.so /usr/lib/libz.so.1
libz.so.1
libbfd-2.24-system.so
/usr/bin/strings,/usr/bin/strings
libselinux.so.1
/usr/lib/libbfd-2.24-system.so,/usr/lib/libbfd-2.24-system.so
/bin/ls,/bin/ls
libacl.so.1
/usr/lib/libz.so.1
libdl.so.2
/bin/cat,/bin/cat
libc.so.6
```

```sh
RDEPS_PATH=/lib:/usr/lib:/sbin/lib ./rdeps.py -r /bin/ls
libattr.so.1,/lib/x86_64-linux-gnu/libattr.so.1
/bin/ls,/bin/ls
libselinux.so.1,/lib/x86_64-linux-gnu/libselinux.so.1
libpcre.so.3,/lib/x86_64-linux-gnu/libpcre.so.3
ld-linux-x86-64.so.2,/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
libacl.so.1,/lib/x86_64-linux-gnu/libacl.so.1
libdl.so.2,/lib/x86_64-linux-gnu/libdl.so.2
libc.so.6,/lib/x86_64-linux-gnu/libc.so.6
```

#### JSON Output

```sh
$ RDEPS_PATH=/lib:/usr/lib:/sbin/lib ./rdeps.py -r /bin/ls -j
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
