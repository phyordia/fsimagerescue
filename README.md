# FSImageRescue

List and Recover Files from APFS images. 

The purpose of this tool is to recover files from APFS formated (external) disks that are unable to mount.
This is an alternative to DiskDrill and all the other paid tools out there.

**Note:** This is highly untested :)

## Requirements
- [dfVFS](https://github.com/log2timeline/dfvfs/wiki)
   - [libfsapfs](https://github.com/libyal/libfsapfs)
      - [The Sleuth Kit](https://github.com/sleuthkit/sleuthkit/)

Make sure you bulid the Python bindings for all the packages.

## Installing dependencies
dfVFS repo and build it according to its installation instructions

### macOS tips

On macOS Mojave, if it fails compiling with and error like `<string>` not found, or that -lstdc++ is not found,
try to set: `export MACOSX_DEPLOYMENT_TARGET=10.14` before `./configure && make`.

# Usage
```
usage: fsimagerescue.py [-h] [--output_dir OUTPUT_DIR] [image.raw]

List or Recover file entries in a directory or storage media image.

positional arguments:
  image.raw             path of the directory or storage media image.

optional arguments:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        path of the output directory to write files to
```

*List files only*
```bash
python fsimagerescue.py testAPFS.dmg
```

*List and save files*
```bash
python fsimagerescue.py --output_dir rescued/ testAPFS.dmg
```