import sys
import argparse
from FSReader import FSReader
import humanize

from colorama import init
init()

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description=('List or Recover file entries in a directory or storage media image.'))

    argument_parser.add_argument('--output_dir', '-o', dest='output_dir', action='store', default=None,
                                 help=('path of the output directory to write files to'))

    argument_parser.add_argument('--deduplicate', '-d', dest='dedup', action='store_true', default=None,
                                 help=('separate duplicate files'))


    argument_parser.add_argument('--resume', '-r', dest='resume', action='store_true', default=None,
                                 help=('continue from last file in the log'))

    argument_parser.add_argument('source', nargs='?', action='store', metavar='image.raw',
        default=None, help='path of the directory or storage media image.')

    options = argument_parser.parse_args()

    img = options.source
    output_dir = options.output_dir

    print("Reading", img)
    print("Saving to", output_dir)

    if not img:
        print("No image to read. Exiting")
        argument_parser.print_help()
        sys.exit(0)


    FSR = FSReader(img, output_dir=output_dir, dedup=options.dedup, resume=options.resume)

    FSR.recover_files()

    print("\n\nFinished\n\n")
    for k,v in FSR.stats.items():
        print("%s: %s"%(k, v if k != "total_size" else humanize.naturalsize(v)))