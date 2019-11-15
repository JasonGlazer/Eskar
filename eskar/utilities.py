import os

class Utilities(object):

    def __init__(self):
        pass

    def delete_file_if_exists(self, target_file_name):
        if os.path.exists(target_file_name):
            os.remove(target_file_name)

    def concatenate_files(self, source_file_one, source_file_two, destination_file):
        with open(destination_file, 'w') as outfile:
            with open(source_file_one) as infile:
                for line in infile:
                    outfile.write(line)
            with open(source_file_two) as infile:
                for line in infile:
                    outfile.write(line)

    def remove_objects(self, list_of_objects, original_file, result_file):
        upper_list_of_objects = [x.upper() for x in list_of_objects]
        with open(result_file, 'w') as outfile:
            with open(original_file) as infile:
                in_object = False
                in_selected_object = False
                for line in infile:
                    write_line = not in_selected_object
                    exclamation_point_loc = line.find('!')
                    comma_loc = line.find(',')
                    # only worry about commas that appear before the comment character '!'
                    if comma_loc > exclamation_point_loc:
                        comma_loc = -1
                    semi_loc = line.find(';')
                    # only worry about semicolons that appear before the comment character '!'
                    if semi_loc > exclamation_point_loc:
                        semi_loc = -1
                    if not in_object:
                        if comma_loc >= 0:
                            in_object = True
                            type_of_object = line[:comma_loc].strip().upper()
                            if type_of_object in upper_list_of_objects:
                                write_line = False
                                in_selected_object = True
                    if in_object:
                        if semi_loc >= 0:
                            in_object = False
                            in_selected_object = False
                    if write_line:
                        outfile.write(line)
                    print(write_line,line)
