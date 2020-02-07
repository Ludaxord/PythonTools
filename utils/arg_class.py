import pathlib
from abc import ABC


class ArgClass(ABC):

    def get_file_path(self):
        return pathlib.Path(__file__).parent.absolute()

    def get_current_dir_path(self):
        return pathlib.Path().absolute()

    def get_args(self):
        pass

    def __args(self):
        pass
