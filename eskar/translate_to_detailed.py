
from eppy import modeleditor
from eppy.modeleditor import IDF


class TranslateToDetailed(object):

    def __init__(self, before_file_name, new_objects_only_file_name):
        self.before_file_name = before_file_name
        self.new_objects_only_file_name = new_objects_only_file_name
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

    def initialize_eppy(self):
        iddfile = "C:\EnergyPlusV9-2-0-Eskar\Energy+.idd"
        IDF.setiddname(iddfile)
        self.idf = IDF(self.before_file_name)

    def do_eksar_objects_exist(self):
        for eskar_object in self.eskar_objects:
            if len(self.idf.idfobjects[eskar_object])>0:
                print(self.idf.idfobjects[eskar_object])
                return True
        return False

    def list_of_eskar_objects(self):
        return self.eskar_objects

    def create_detailed_objects(self):
        pass




