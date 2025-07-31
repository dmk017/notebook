import os

import magic
import xmltodict

import requests


class NextCloudAPI:
    def __init__(self, instance, user, password, nc_folder_path='/public') -> None:
        """
        @nc_folder_path - IMPORTANT check this folder exist on server
        """
        self.__instance_ocs = f"{instance}/ocs"
        self.__instance_dav = f"{instance}/remote.php/dav"

        self.__user = user
        self.__password = password

        self.__nc_folder_path = nc_folder_path

        self.__session = requests.Session()
        self.__session.auth = (self.__user, self.__password)
        self.__session.headers.update({'OCS-APIRequest': 'true'})

    def get_users(self):
        response = self.__session.get(self.__instance_ocs + '/v1.php/cloud/users')
        return self.__decode_xml_to_dict(response.text)

    def upload_local_file(self, file_path):
        if not os.path.exists(file_path):
            return self.__build_response(
                False,
                'File not found on path'
            )

        content_type = self.__get_mime_type(file_path)
        return self.upload_file(
            file=open(file_path, 'rb'),
            file_name=file_path,
            content_type=content_type
        )

    def upload_file(self, file, file_name, content_type):
        """
        @param file - binary file to uplod
        @param file_name - name file on NextCloud
        @param content_type - file mime type
        """
        headers = {'Content-type': content_type}
        nc_file_path = self.__build_nc_path(file_name)
        response = self.__session.put(
            url=f"{self.__instance_dav}/files/{self.__user}{nc_file_path}",
            data=file,
            headers=headers
        )
        message = ''
        if response.status_code == 201:
            message = 'Success to upload file'
        elif response.status_code == 204:
            message = 'Success update file'
        else:
            return self.__build_response(
                False,
                'File upload error'
            )
        return self.__build_response(
            True,
            message,
            data={
                "nc_path": nc_file_path
            }
        )

    def download_file(self, nc_file_path):
        response = self.__session.get(
            url=f"{self.__instance_dav}/files/{self.__user}{nc_file_path}"
        )
        return response.content

    def __build_nc_path(self, file_path):
        return os.path.join(self.__nc_folder_path, os.path.basename(file_path))

    @staticmethod
    def __get_mime_type(file_path):
        return magic.from_file(file_path, mime=True)

    @staticmethod
    def __decode_xml_to_dict(response):
        return xmltodict.parse(response)

    @staticmethod
    def __build_response(success, message='', data={}):
        return {
            "success": success,
            "message": message,
            "data": data
        }
