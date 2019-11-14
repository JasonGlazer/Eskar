
from eppy import modeleditor
from eppy.modeleditor import IDF


class TranslateToDetailed(object):

    def __init__(self, file_name):
        self.file_name = file_name
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
        self.idf = IDF(self.file_name)

    def do_eksar_objects_exist(self):
        print('do_eksar_objects_exist')
        print(self.file_name)


