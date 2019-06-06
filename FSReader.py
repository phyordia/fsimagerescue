#This requires installing dfvfs, pytsk (whih includes sleuthkit)


import logging
import os
from dfvfs.analyzer import analyzer
from dfvfs.analyzer import fvde_analyzer_helper
from dfvfs.helpers import command_line
from dfvfs.helpers import volume_scanner
from dfvfs.lib import errors
from dfvfs.resolver import resolver
from OutputWriters import FileOutputWriter
from EntryObject import EntryObject

class FSReader:
    def __init__(self, img, output_dir=None, dedup=False, log_file=None):

        self.img = img
        # mkdirs
        if output_dir:
            self.output_dir = os.path.abspath(output_dir+"/"+self.img)
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

            if dedup:
                self.dedup_dir = self.output_dir+"_duplicates"
                if not os.path.exists(self.dedup_dir):
                    os.makedirs(self.dedup_dir)

        mediator = command_line.CLIVolumeScannerMediator()
        vol_scanner = volume_scanner.VolumeScanner(mediator=mediator)
        self.stats = {"errors": 0, "total": 0, "duplicates": 0}
        self.hashes = {}
        self.base_path_specs = vol_scanner.GetBasePathSpecs(img)

        self.last_file = None
        self.log_file = FileOutputWriter(log_file) if log_file else None
        self.err_log_file = FileOutputWriter(log_file+".err.txt") if log_file else None


        if self.log_file:
            self.log_file.Open()
            self.err_log_file.Open()


    def _ListFileEntry(self, file_system, file_entry, parent_full_path):
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
        this_obj = EntryObject(file_entry, full_path)

        # Check hashes
        if file_entry.entry_type=="file" and this_obj.size:
            if self.hashes.get(this_obj.hash):
                this_obj.duplicate = ",".join(self.hashes.get(this_obj.hash))
                self.hashes[this_obj.hash].append(full_path)
            else:
                self.hashes[this_obj.hash] = [full_path]

        this_obj.log(self.log_file)




        # Update Stats
        self.stats['total'] += 1
        self.stats[file_entry.entry_type] = self.stats[file_entry.entry_type]+1 if self.stats.get(file_entry.entry_type) else 1
        if this_obj.duplicate:
            self.stats['duplicates'] += 1



        #     print(full_path)
        #     if not self._list_only_files or file_entry.IsFile():
        # self.log_object(file_entry, full_path)
        # self.stats['found'] += 1
        # if output_dir:
        #     self.save_object(file_entry, full_path, output_dir)


        for sub_file_entry in file_entry.sub_file_entries:
            self._ListFileEntry(file_system, sub_file_entry, full_path)


    def recover_files(self, output_dir=None):
        for base_path_spec in self.base_path_specs:
            file_system = resolver.Resolver.OpenFileSystem(base_path_spec)
            file_entry = resolver.Resolver.OpenFileEntry(base_path_spec)

            if file_entry is None:
                print('Unable to open base path specification:\n{0:s}'.format(base_path_spec.comparable))
                return
            self._ListFileEntry(file_system, file_entry, '')

        if self.log_file:
            self.log_file.Close()
            self.err_log_file.Close()

