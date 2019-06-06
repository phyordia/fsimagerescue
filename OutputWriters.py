import logging
import abc


class OutputWriter:
    """Output writer interface."""

    def __init__(self, encoding='utf-8'):
        """Initializes an output writer.

        Args:
          encoding (Optional[str]): input encoding.
        """

        self._encoding = encoding
        self._errors = 'strict'

    def _EncodeString(self, string):
        """Encodes the string.

        Args:
          string (str): string to encode.

        Returns:
          bytes: encoded string.
        """
        try:
            # Note that encode() will first convert string into a Unicode string
            # if necessary.
            encoded_string = string.encode(self._encoding, errors=self._errors)
        except UnicodeEncodeError:
            if self._errors == 'strict':
                logging.error(
                    'Unable to properly write output due to encoding error. '
                    'Switching to error tolerant encoding which can result in '
                    'non Basic Latin (C0) characters to be replaced with "?" or '
                    '"\\ufffd".')
                self._errors = 'replace'

            encoded_string = string.encode(self._encoding, errors=self._errors)

        return encoded_string

    @abc.abstractmethod
    def Close(self):
        """Closes the output writer object."""

    @abc.abstractmethod
    def Open(self):
        """Opens the output writer object."""

    @abc.abstractmethod
    def WriteFileEntry(self, path):
        """Writes the file path.

        Args:
          path (str): path of the file.
        """



class FileOutputWriter(OutputWriter):
    """Output writer that writes to a file."""

    def __init__(self, path, encoding='utf-8'):
        """Initializes an output writer.

        Args:
          path (str): name of the path.
          encoding (Optional[str]): input encoding.
        """
        super(FileOutputWriter, self).__init__(encoding=encoding)
        self._file_object = None
        self._path = path

    def Close(self):
        """Closes the output writer object."""
        self._file_object.close()

    def Open(self):
        """Opens the output writer object."""
        # Using binary mode to make sure to write Unix end of lines, so we can
        # compare output files cross-platform.
        self._file_object = open(self._path, 'wb')
        self.WriteFileEntry("entry_type,size,full_path,hash,duplicate")

    def WriteFileEntry(self, s):
        """Writes the file path to file.

        Args:
          path (str): path of the file.
        """
        s = '{0:s}\n'.format(s)

        encoded_string = self._EncodeString(s)
        self._file_object.write(encoded_string)