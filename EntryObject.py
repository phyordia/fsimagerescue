import hashlib

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
        self.hash = 123

        f_obj.close()


    def log(self, writer):
        # "entry_type,size,full_path,hash,duplicate"
        s = "%s,%s,%s,%s,%s" % (self.obj.entry_type, self.size, self.full_path, self.hash, self.duplicate)

        #TODO add a quiet mode
        print(s)

        writer.WriteFileEntry(s)
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