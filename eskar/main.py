import sys
import os
import shutil

from eskar.translate_to_detailed import TranslateToDetailed
from eskar.utilities import Utilities

def main():
    if len(sys.argv) == 2:
        before_file_name = sys.argv[1]
        if os.path.exists(before_file_name):
            utility = Utilities()
            root, ext = os.path.splitext(before_file_name)

            # the "after_file" is the eventual name of the file that is given to the user
            after_file_name = root + '-after' + ext
            utility.delete_file_if_exists(after_file_name)

            # a temporary file that contains only the new objects created
            new_objects_only_file_name = root + '-new-objects-only.temp'
            utility.delete_file_if_exists(new_objects_only_file_name)

            # the original file but with Eskar objects removed
            with_objects_removed_file_name = root + '-with-objects-removed.temp'
            utility.delete_file_if_exists(with_objects_removed_file_name)

            # errors and warnings file
            warnings_file_name = root + '-eskar.err'
            utility.delete_file_if_exists(warnings_file_name)

            translator = TranslateToDetailed(before_file_name, new_objects_only_file_name, warnings_file_name)
            if translator.do_eksar_objects_exist():
                translator.create_detailed_objects()
                list_of_object_names = translator.list_of_eskar_objects()
                utility.remove_objects(list_of_object_names, before_file_name, with_objects_removed_file_name)
                utility.concatenate_files(with_objects_removed_file_name, new_objects_only_file_name, after_file_name)
                # clean up the temporary files
#                utility.delete_file_if_exists(new_objects_only_file_name)
#                utility.delete_file_if_exists(with_objects_removed_file_name)
                translator.close_warnings_file()
            else:
                os.remove(after_file_name)
                print('No Eskar:* objects found in the file: ', before_file_name)
        else:
            print('The file {} was not found'.format(before_file_name))
    else:
        print('Please include the file name on the command line in the form: Eskar <filename>')
        print('If the file name with path includes spaces please include it in quotes.')

if __name__ == '__main__':
    sys.exit(main())
