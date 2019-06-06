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
usage: fsimagerescue.py [-h] [--output_dir OUTPUT_DIR] [--log LOG_FILE]
                        [image.raw]

List or Recover file entries in a directory or storage media image.

positional arguments:
  image.raw             path of the directory or storage media image.

optional arguments:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        path of the output directory to write files to
  --log LOG_FILE, -l LOG_FILE
                        path of the log file
```

*List files only*
```bash
python fsimagerescue.py testAPFS.dmg
```

*List and save files*
```bash
python fsimagerescue.py --output_dir rescued/ --log fsimage.log.txt testAPFS.dmg
```


## Output

The output format is "<size in bytes (files) or "dd" (directory)>,<path>"

Example:
```
[...]
45,/DIY Pedals/schematics/output/mu-amp_OD-Distortion.png.txt
67,/DIY Pedals/schematics/output/out.png.txt
270,/DIY Pedals/schematics/output/jfet_ac30.png.txt
138,/DIY Pedals/schematics/output/fuzzfaceout.png.txt
51806,/DIY Pedals/schematics/output/jfet_ac30.png
128,/DIY Pedals/schematics/output/jfet_clean_boost.png.txt
0,/DIY Pedals/schematics/output/result.png.txt
81999,/DIY Pedals/schematics/fuzzface.png
50993,/DIY Pedals/schematics/jfet_clean_boost.png
89134,/DIY Pedals/schematics/jfet_ac30.png
1118,/DIY Pedals/schematics/mask.png
76925,/DIY Pedals/schematics/result-0.png
1118,/DIY Pedals/schematics/result-1.png


Finished

<<<<<<< HEAD
 {'dirs': 6, 'rescued': 51, 'errors': 0, 'found': 57}

```
=======
{'dirs': 6, 'rescued': 51, 'errors': 0, 'found': 57}
```


# Aknowledgment
Thanks to Joachim Metz for all the help with dfvfs!
>>>>>>> 240ddfe3f9d97189ed5add566e17c023ea61a72b
