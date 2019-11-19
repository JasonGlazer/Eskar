
from eppy import modeleditor
from eppy.modeleditor import IDF


class TranslateToDetailed(object):

    def __init__(self, before_file_name, new_objects_only_file_name, warnings_file_name):
        self.before_file_name = before_file_name
        self.new_objects_only_file_name = new_objects_only_file_name
        self.warnings_file_name = warnings_file_name
        self.warning_file = open(warnings_file_name,'w')
        self.initialize_eppy()
        self.eskar_objects = ['Eskar:Heights',
                              'Eskar:DimensionSeriesX',
                              'Eskar:DimensionSeriesY',
                              'Eskar:Zone',
                              'Eskar:OccupancyType',
                              'Eskar:Defaults',
                              'Eskar:VerticalDetails',
                              'Eskar:HorizontalDetails',
                              'Eskar:DetachedShading',
                              'Eskar:RoofShape',
                              'Eskar:Override',
                              'Eskar:Libary']
        self.created_detailed_objects = {}
        self.heights_at_indices = self.process_eskar_height_objects()
        self.x_distances = self.process_eskar_dimension_series('X')
        self.y_distances = self.process_eskar_dimension_series('Y')

    def initialize_eppy(self):
        iddfile = "C:\EnergyPlusV9-2-0-Eskar\Energy+.idd"
        IDF.setiddname(iddfile)
        self.idf = IDF(self.before_file_name)

    def close_warnings_file(self):
        self.warning_file.close()

    def do_eksar_objects_exist(self):
        for eskar_object in self.eskar_objects:
            if len(self.idf.idfobjects[eskar_object])>0:
                # print(self.idf.idfobjects[eskar_object])
                return True
        return False

    def list_of_eskar_objects(self):
        return self.eskar_objects

    def new_object_and_collect(self, object_type, **kwargs):
        self.created_detailed_objects.setdefault(object_type, [])
        new_object = self.idf.newidfobject(object_type, **kwargs)
        self.created_detailed_objects[object_type].append(new_object)
        return new_object

    def write_new_objects_to_file(self):
        object_strings = []
        for key in self.created_detailed_objects.keys():
            for an_object in self.created_detailed_objects[key]:
                object_strings.append(str(an_object))
        with open(self.new_objects_only_file_name, 'w') as outfile:
            for line in object_strings:
                outfile.write(line + '\n')

    def create_detailed_objects(self):
        self.get_eskar_objects()
        self.new_object_and_collect("ZONE", Name='zone1')
        self.write_zone_geometry()
        self.write_new_objects_to_file()

    def get_eskar_objects(self):

        self.eskar_dimension_series_x = self.idf.idfobjects['Eskar:DimensionSeriesX']
        if len(self.eskar_dimension_series_x) != 1:
            self.warning_file.write('Every file with Eskar objects should have one and only one Eskar:DimensionSeriesX object.\n')

        self.eskar_dimension_series_y = self.idf.idfobjects['Eskar:DimensionSeriesY']
        if len(self.eskar_dimension_series_y) != 1:
            self.warning_file.write('Every file with Eskar objects should have one and only one Eskar:DimensionSeriesY object.\n')

        self.eskar_defaults = self.idf.idfobjects['Eskar:Defaults']
        if len(self.eskar_defaults) > 1:
            self.warning_file.write('Every file with Eskar objects should have no more than one Eskar:Defaults object.\n')

        self.eskar_library = self.idf.idfobjects['Eskar:Libary']
        if len(self.eskar_library) > 1:
            self.warning_file.write('Every file with Eskar objects should have no more than one Eskar:Libary object.\n')

        self.eskar_zones = self.idf.idfobjects['Eskar:Zone']

        self.eskar_occupancy_types = self.idf.idfobjects['Eskar:OccupancyType']
        self.eskar_vertical_details = self.idf.idfobjects['Eskar:VerticalDetails']
        self.eskar_horizonal_details = self.idf.idfobjects['Eskar:HorizontalDetails']
        self.eskar_detached_shadings = self.idf.idfobjects['Eskar:DetachedShading']
        self.eskar_roof_shapes = self.idf.idfobjects['Eskar:RoofShape']
        self.eskar_overrides = self.idf.idfobjects['Eskar:Override']

    def process_eskar_height_objects(self):
        eskar_heights = self.idf.idfobjects['Eskar:Heights']
        if len(eskar_heights) != 1:
            self.warning_file.write('Every file with Eskar objects should have one and only one Eskar:Heights object.\n')
        current_height = 0
        heights_at_indices = []
        current_eskar_heights_object = eskar_heights[0]
        for fld in current_eskar_heights_object.fieldnames:
            if fld == 'Name' or fld == 'key':
                continue
            if fld:
                if current_eskar_heights_object[fld] != '': # this needs to have this comparison with blank since the 0 seems to be false also even though a string
                    if self.is_number(current_eskar_heights_object[fld]):
                        incremental_height = float(current_eskar_heights_object[fld])
                        if abs(incremental_height) < 10000:
                            current_height += incremental_height
                            heights_at_indices.append(current_height)
                        else:
                            # special "reset" function when using very large or very negative number
                            current_height = 0
                            heights_at_indices.append(0)
                    else:
                        self.warning_file.write('Non-numeric value found in Eskar:Heights for field: {} with value of \"{}\".\n'.format(fld,current_eskar_heights_object[fld]))
                # else:
                #    print(fld,current_eskar_heights_object[fld])
            else:
                break # no blank lines
        print('heights_at_indices ', heights_at_indices)
        return heights_at_indices

    def process_eskar_dimension_series(self, x_or_y):
        eskar_dimension_series = self.idf.idfobjects['Eskar:DimensionSeries'+ x_or_y]
        if len(eskar_dimension_series) != 1:
            self.warning_file.write('Every file with Eskar objects should have one and only one Eskar:DimensionSeries{} object.\n'.format(x_or_y))
        current_distance = 0
        distance_at_indices = []
        current_eskar_dimension_series_object = eskar_dimension_series[0]
        for fld in current_eskar_dimension_series_object.fieldnames:
            if fld == 'Name' or fld == 'key':
                continue
            if fld:
                if current_eskar_dimension_series_object[fld] != '': # this needs to have this comparison with blank since the 0 seems to be false also even though a string
                    if self.is_number(current_eskar_dimension_series_object[fld]):
                        incremental_distance = float(current_eskar_dimension_series_object[fld])
                        if abs(incremental_distance) < 10000:
                            current_distance += incremental_distance
                            distance_at_indices.append(current_distance)
                        else:
                            # special "reset" function when using very large or very negative number
                            current_distance = 0
                            distance_at_indices.append(0)
                    else:
                        self.warning_file.write('Non-numeric value found in Eskar:DimensionSeries{} for field: {} with value of \"{}\".\n'.format(x_or_y, fld, current_eskar_dimension_series_object[fld]))
                # else:
                #    print(fld,current_eskar_dimension_series_object[fld])
            else:
                break # no blank lines
        print('distance_at_indices for {} is {}'.format(x_or_y, distance_at_indices))
        return distance_at_indices

    def height_from_height_index(self, height_index):
        if self.is_number(height_index):
            if height_index <= len(self.heights_at_indices):
                return self.heights_at_indices[height_index]
            else:
                self.warning_file.write('Invalid height index reference of \"{}\" it must be consistent with values entered in Eskar:Height.  \n'.format(height_index))
                return 0
        else:
            self.warning_file.write('Reference to a height index of \"{}\" is invalid. Only integer numbers are allowed for height indices. \n'.format(height_index))
            return 0

    def write_zone_geometry(self):
        for zone in self.eskar_zones:
            # self.print_field_names(zone)
            # print(zone)
            floor_height = self.height_from_height_index(zone.Height_index_of_Floor )
            ceiling_height = self.height_from_height_index(zone.Height_index_of_Floor )
            next_floor_height = self.height_from_height_index(zone.Height_index_of_Next_Floor)
            break
            for fld in zone.fieldnames:
                if 'corner' in fld:
                    corner_x, corner_y = self.xy_position_from_corner_code(zone[fld])
                    print(corner_x, ',', corner_y)


    def print_field_names(self, ep_obj):
        print()
        for fld in ep_obj.fieldnames:
            if fld == 'key':
                print(ep_obj[fld])
            else:
                if self.is_number(ep_obj[fld]):
                    print("    obj.{} = {} ".format(fld, ep_obj[fld]))
                else:
                    print("    obj.{} = '' ".format(fld))

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
