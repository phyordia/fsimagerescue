#This requires installing dfvfs, pytsk (whih includes sleuthkit)


import os
import sys
import logging
from dfvfs.analyzer import analyzer
from dfvfs.analyzer import fvde_analyzer_helper
from dfvfs.helpers import command_line
from dfvfs.helpers import volume_scanner
from dfvfs.lib import errors
from dfvfs.resolver import resolver
from OutputWriters import FileOutputWriter
import argparse



class FSReader:
    def __init__(self, img, log_file=None):

        mediator = command_line.CLIVolumeScannerMediator()
        vol_scanner = volume_scanner.VolumeScanner(mediator=mediator)
        self.stats = {"dirs": 0, "rescued":0, "errors": 0, "found": 0}
        self.base_path_specs = vol_scanner.GetBasePathSpecs(img)
        self.last_file = None
        self.log_file = FileOutputWriter(log_file) if log_file else None

        if self.log_file:
            self.log_file.Open()

    def log_object(self, o, full_path):
        f_obj = o.GetFileObject()

        s = "%s,%s,%s" % (o.entry_type, f_obj.get_size(), full_path)
        print(s)
        if self.log_file:
            self.log_file.WriteFileEntry(s)

        f_obj.close()

    def save_object(self, o, full_path, output_dir):
        save_to = os.path.abspath(output_dir + "/" + full_path)
        f_obj = o.GetFileObject()

        if o.IsDirectory():
            try:
                if not os.path.exists(save_to):
                    os.makedirs(save_to)
                    self.stats['dirs'] += 1
            except Exception as e:
                print("Cannot create directory '%s'"%save_to)
                self.stats['errors'] += 1

        elif o.IsFile():
            try:
                with open(save_to, "wb") as f:
                    f.write(f_obj.read())
                    self.stats['rescued'] += 1
            except Exception as e:
                print("Cannot create file '%s'" % save_to)
                print(e)
                self.stats['errors'] += 1

        f_obj.close()

    def _ListFileEntry(self, file_system, file_entry, parent_full_path, output_dir=None):
        """Lists a file entry.

        Args:
          file_system (dfvfs.FileSystem): file system that contains the file entry.
          file_entry (dfvfs.FileEntry): file entry to list.
          parent_full_path (str): full path of the parent file entry.
          output_writer (StdoutWriter): output writer.
        """
        # Since every file system implementation can have their own path
        # segment separator we are using JoinPath to be platform and file system
        # type independent.
        self.last_file = file_entry
        # file_entry_f = file_entry.GetFileObject()

        full_path = file_system.JoinPath([parent_full_path, file_entry.name])
        #     print(full_path)
        #     if not self._list_only_files or file_entry.IsFile():
        self.log_object(file_entry, full_path)
        self.stats['found'] += 1
        if output_dir:
            self.save_object(file_entry, full_path, output_dir)


        for sub_file_entry in file_entry.sub_file_entries:
            self._ListFileEntry(file_system, sub_file_entry, full_path, output_dir)


    def recover_files(self, output_dir=None):
        for base_path_spec in self.base_path_specs:
            file_system = resolver.Resolver.OpenFileSystem(base_path_spec)
            file_entry = resolver.Resolver.OpenFileEntry(base_path_spec)

            if file_entry is None:
                print('Unable to open base path specification:\n{0:s}'.format(base_path_spec.comparable))
                return
            self._ListFileEntry(file_system, file_entry, '', output_dir=output_dir)

        if self.log_file:
            self.log_file.Close()




if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(description=('List or Recover file entries in a directory or storage media image.'))

    argument_parser.add_argument('--output_dir', '-o', dest='output_dir', action='store', default=None,
                                 help=('path of the output directory to write files to'))

    argument_parser.add_argument('--log', '-l', dest='log_file', action='store', default=None,
                                 help=('path of the log file'))

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


    FSR = FSReader(img, log_file=options.log_file)

    FSR.recover_files(output_dir=output_dir)

    print("\n\nFinished\n\n",FSR.stats)