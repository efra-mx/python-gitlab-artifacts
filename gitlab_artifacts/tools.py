import os, shutil
import tempfile
from zipfile import ZipFile 


def get_list_of_files(dir_name):
    '''
        For the given path, get the List of all files in the directory tree
    '''
    # create a list of file and sub directories
    # names in the given directory
    _list_of_file = os.listdir(dir_name)
    all_files = list()
    all_rel_files = list()
    # Iterate over all the entries
    for entry in _list_of_file:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            _all_files, _rel_files = get_list_of_files(full_path)
            all_files = all_files + _all_files
            all_rel_files = all_rel_files + _rel_files
        else:
            all_files.append(full_path)
            all_rel_files.append(entry)

    return all_files, all_rel_files


def clean_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


class ZipWriter(object):
    def __init__(self, output_file):
        self._output_file = output_file

        self._fd = open(self._output_file, 'wb')

    def __call__(self, chunk):
        self._fd.write(chunk)

    def output_file(self):
        return self._output_file
    

class ZipReader(object):
    def __init__(self, input_file):
        self._input_file = input_file
        self._files = []
        self._folder = ""

    def unzip(self, output_path, pristine=True):
        if not output_path:
            output_path = tempfile.mkdtemp()
        elif os.path.isdir(output_path) and pristine:
            clean_folder(output_path)
            self._folder = output_path
            
        if os.path.isfile(self._input_file):
            # unzip
            with ZipFile(self._input_file, 'r') as z_object: 
            
                # Extracting all the members of the zip  
                # into a specific location. 
                z_object.extractall(path=output_path)
                self._files = z_object.namelist()
                if self._folder:
                    print("output folder:", output_path)

    def list_files(self):
        if self._folder:
            print("Files:")
        else:
            print("Unzipped files:")
        if self._files:
            [ print(f"\t{f}") for f in self._files ]

    @property
    def files(self):
        return self._files
