from rest_framework import serializers

import shutil

from .models import *

class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length = 100000, allow_empty_file=False, use_url=False)
    )

    def zip_files(self, folder):
        shutil.make_archive(f"static/images/zip/{folder}", 'zip', f"static/images/zip/{folder}")


    def create(self, validated_data):
        folder = Folder.objects.create()
        files = validated_data.pop('files')
        file_objs = []
        for file in files:
            file_obj = Files.objects.create(folder=folder, file=file)
            file_objs.append(file_obj)

        # serialized_files = [{'file': str(file_obj.file), 'created': file_obj.created} for file_obj in file_objs]

        self.zip_files(str(folder.uid))

        return {"files":{}, "folder": str(folder.uid)}
