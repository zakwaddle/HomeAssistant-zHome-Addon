from FTPUploader import FTPUploader
import json
import os


class FirmwareUploader:
    local_firmware_folder = os.path.abspath(f"{os.path.dirname(__file__)}/../Firmware")
    local_home_path = f"{local_firmware_folder}/dist"

    ftp_home_folder = f"/upload/Firmware"

    def __init__(self):
        self.ftp_uploader = FTPUploader(host="homeassistant.local",
                                        user="microcontrollers",
                                        password="microcontrollers")
        self.ftp_uploader.set_excluded_files([".gitignore", ".gitattributes", ".git"])

    def clear(self):
        print("uploading unit folder")
        self.ftp_uploader.connect()
        self.ftp_uploader.clear_folder(self.ftp_home_folder)
        self.ftp_uploader.disconnect()

    def create_home_package_folder(self):
        self.ftp_uploader.connect()
        self.ftp_uploader.create_directory("/upload")
        self.ftp_uploader.create_directory(self.ftp_home_folder)
        self.ftp_uploader.disconnect()

    def create_package_manifest(self):
        manifest = {
            "package_root": self.ftp_home_folder,
            "directories": [i.removeprefix(self.ftp_home_folder) for i in self.ftp_uploader.uploaded_directories],
            "files": [i.removeprefix(self.ftp_home_folder) for i in self.ftp_uploader.uploaded_files]
        }
        with open('./manifest.json', 'w') as file:
            json.dump(manifest, file)
        self.ftp_uploader.uploaded_files = []
        self.ftp_uploader.uploaded_directories = []

    def upload_manifest(self):
        self.ftp_uploader.upload_file('./manifest.json', f'{self.ftp_home_folder}/manifest.json')

    def upload_home_package(self):
        # self.ftp_uploader.create_directory("/upload/Firmware")

        self.create_home_package_folder()
        print("clearing home folder")
        self.ftp_uploader.clear_folder(self.ftp_home_folder)
        print("uploading home folder")
        self.ftp_uploader.upload_folder(self.local_home_path, self.ftp_home_folder)
        self.create_package_manifest()
        print("uploading manifest")
        self.ftp_uploader.connect()
        self.upload_manifest()
        self.ftp_uploader.disconnect()


if __name__ == "__main__":
    uploader = FirmwareUploader()
    uploader.upload_home_package()

