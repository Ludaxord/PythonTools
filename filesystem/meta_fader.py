#!/usr/bin/env python3

from PIL import Image, ExifTags

from utils.arg_class import ArgClass
from utils.parser import Parser


class MetaFader(ArgClass):
    file_path = None

    def __init__(self, file_path=None):
        if file_path is not None:
            self.file_path = file_path

    def __args(self):
        return Parser(args=[{"command": "--path", "type": str, "help": "full path to image file"},
                            {"command": "--new_path", "type": str,
                             "help": "full path to new image file"}]).get_args()

    def get_args(self):
        args = self.__args()
        path = args.path
        new_file_path = args.new_path
        return path, new_file_path

    def meta_display(self, file_path=None):
        if file_path is None:
            file_path = self.file_path
        image = Image.open(file_path)
        exif = self.get_meta(image)
        return exif

    def get_meta(self, image):
        try:
            exif = {ExifTags.TAGS[k]: v for k, v in image._getexif().items() if k in ExifTags.TAGS}
        except Exception as e:
            print(f"{e}")
            exif = {}
        return exif

    def decode_maker_note(self, exif):
        maker_note = exif.get("MakerNote")
        maker_notes = [maker_note[i:i + 1] for i in range(0, len(maker_note), 1)]
        encodings = ['utf-8', 'utf-16', 'ascii', 'base64']
        print(f"encoding {encodings}")
        decoded = []
        for encoding in encodings:
            decoded_note = ""
            for note in maker_notes:
                try:
                    decoded_note += note.decode(encoding)
                except Exception as e:
                    exception = e
            decoded.append(decoded_note)
        return decoded

    def meta_remove(self, save_file, file_path=None, new_file_path=None):
        if file_path is None:
            file_path = self.file_path
        image = Image.open(file_path)
        data = list(image.getdata())
        removed_data_image = Image.new(image.mode, image.size)
        removed_data_image.putdata(data)
        if save_file:
            if new_file_path is None:
                new_file_path = file_path
            removed_data_image.save(new_file_path)
        return removed_data_image


meta = MetaFader()

path, new_file_path = meta.get_args()

exif = meta.meta_display(file_path=path)

print(exif)

new_image = meta.meta_remove(True, new_file_path=new_file_path)

new_exif = meta.meta_display(file_path=new_file_path)

print(new_exif)
