import sys
import os

from eskar.translate_to_detailed import TranslateToDetailed


def main():
    if len(sys.argv) == 1:
        input_file_name = sys.argv[1]
        print('input_file_name',input_file_name)
        if os.path.exists(input_file_name):
            translator = TranslateToDetailed(input_file_name)
            if translator.do_eksar_objects_exist():
                pass


if __name__ == '__main__':
    sys.exit(main())
