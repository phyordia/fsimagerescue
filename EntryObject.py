import hashlib
import os
import shutil

class EntryObject:

    def __init__(self, obj, full_path):
        self.obj = obj
        self.full_path = full_path
        self.duplicate = False

        f_obj = self.obj.GetFileObject()
        # Get Size
        f_obj.seek(0,2)
        self.size = f_obj.tell()
        f_obj.seek(0)
        # to do
        BLOCKSIZE = 65536
        m = hashlib.sha256()
        file_buffer = f_obj.read(BLOCKSIZE)
        while len(file_buffer) > 0:
            m.update(file_buffer)
            file_buffer = f_obj.read(BLOCKSIZE)
        self.hash = m.hexdigest()

        f_obj.close()


    def log(self, writer):
        # "entry_type,size,full_path,hash,duplicate"
        s = "%s|%s|%s|%s|%s" % (self.obj.entry_type, self.size, self.full_path, self.hash, self.duplicate)

        #TODO add a quiet mode
        print(s)

        writer.WriteFileEntry(s)

    def store(self, output_dir):
        save_to = os.path.abspath(output_dir + "/" + self.full_path)

        if self.obj.IsDirectory():
            if not os.path.exists(save_to):
                os.makedirs(save_to, exist_ok=True)

        elif self.obj.IsFile():
            dirname = os.path.dirname(save_to)
            if not os.path.exists(dirname):
                os.makedirs(dirname, exist_ok=True)

            f_obj = self.obj.GetFileObject()
            with open(save_to, "wb") as f:
                shutil.copyfileobj(f_obj, f)
            f_obj.close()

    #
    #
    #
    # def log_object(self, o, full_path):
    #     f_obj = o.GetFileObject()
    #
    #     s = "%s,%s,%s" % (o.entry_type, f_obj.get_size(), full_path)
    #     print(s)
    #     if self.log_file:
    #         self.log_file.WriteFileEntry(s)
    #
    #     f_obj.close()
    #
    # def save_object(self, o, full_path, output_dir):
    #     save_to = os.path.abspath(output_dir + "/" + full_path)
    #     f_obj = o.GetFileObject()
    #
    #     if o.IsDirectory():
    #         try:
    #             if not os.path.exists(save_to):
    #                 os.makedirs(save_to)
    #                 self.stats['dirs'] += 1
    #         except Exception as e:
    #             print("Cannot create directory '%s'"%save_to)
    #             self.stats['errors'] += 1
    #
    #     elif o.IsFile():
    #         try:
    #             with open(save_to, "wb") as f:
    #                 f.write(f_obj.read())
    #                 self.stats['rescued'] += 1
    #         except Exception as e:
    #             print("Cannot create file '%s'" % save_to)
    #             print(e)
    #             self.stats['errors'] += 1
    #
    #     f_obj.close()