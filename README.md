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

