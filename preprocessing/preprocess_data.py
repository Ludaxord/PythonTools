import pandas as pd

from utils.arg_class import ArgClass


class PreProcessData(ArgClass):

    encodings = ['utf-8', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256',
                 'cp1257',
                 'cp1258', 'iso8859_15', 'iso8859_16']

    def __init__(self, filename):
        self.file_name = filename
        pass

    def get_encoded_datasets(self, encodings=None):
        accepted_datasets = []
        if encodings is None:
            encodings = self.encodings
        for encoding in encodings:
            try:
                dataset = self.get_dataset(encoding)
                accepted_datasets.append(dataset)
            except Exception as e:
                print(e)
        return accepted_datasets

    def get_accepted_encodings(self):
        accepted_encodings = []
        for encoding in self.encodings:
            try:
                self.get_dataset(encoding)
                accepted_encodings.append(encoding)
            except Exception as e:
                print(e)
        return accepted_encodings

    def get_dataset(self, encoding):
        filename = self.file_name
        dataset = pd.read_csv(filename, delimiter=';', encoding=encoding)
        return dataset

