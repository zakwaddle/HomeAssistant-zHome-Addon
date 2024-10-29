import json
import os
import uos
from .lib.ftplib import FTP
import errno


class DownloadError(Exception):
    pass


class UpdateError(Exception):
    pass


class FTPClient:
    """
    FTPClient class provides a high-level interface to perform operations
    on an FTP server such as connecting, disconnecting, and transferring files.
    """

    def __init__(self, host, user, password):
        """
        Constructs an FTPClient with provided FTP server details.

        :param host: The FTP host address.
        :param user: The username for the FTP host.
        :param password: The password for the FTP host.
        """
        self.host = host
        self.user = user
        self.password = password
        self.ftp = None

    def connect(self):
        """
        Establishes a connection to the FTP server using the host, user, and password
        provided during the initialization of the FTPClient instance.
        """
        self.ftp = FTP()
        self.ftp.connect(self.host)
        self.ftp.login(self.user, self.password)
        print('connected ftp')

    def disconnect(self):
        """
        Disconnects from the FTP server if a connection is established.
        """
        if self.ftp:
            self.ftp.quit()
            print('disconnected ftp')

    def download_file(self, remote_file_path, local_file_path):
        """
        Downloads a file from the FTP server.

        :param remote_file_path: The path of the file on the FTP server.
        :param local_file_path: The path where the file will be saved locally.
        """
        print(f"Remote file path: {remote_file_path}")
        print(f"Local file path: {local_file_path}")
        try:
            with open(local_file_path, "wb") as local_file:
                self.ftp.retrbinary("RETR " + remote_file_path, local_file.write)
        except Exception as e:
            print("Error downloading file:", e)
            raise

    def upload_file(self, local_path, remote_path):
        """
        Uploads a file to the FTP server.

        :param local_path: The path of the file on the local system.
        :param remote_path: The path where the file will be saved on the FTP server.
        """
        with open(local_path, "rb") as f:
            self.ftp.storbinary("STOR " + remote_path, f)

    def change_directory(self, path):
        """
        Changes the current directory on the FTP server.

        :param path: The path of the directory to change to on the FTP server.
        """
        self.ftp.cwd(path)

    def list_directory(self, **kwargs):
        """
        Lists the contents of the current directory on the FTP server.

        :return: A list of the names of the files and directories in the current directory.
        """
        return self.ftp.dir(**kwargs)

    def makepasv(self):
        self.ftp.makepasv()


class HomeUpdate:
    ftp: FTPClient = None
    remote_manifest_path: str = None
    manifest: dict = None
    package_root: str = None
    manifest_directories: list = None
    manifest_files: list = None

    @staticmethod
    def item_is_file(item):
        return uos.stat(f"/{item}")[0] == 0x8000

    @staticmethod
    def update_file(target, source_filepath):
        """
        Overwrites a local file with the contents of another local file.
        :param target: The path of the file to be updated.
        :param source_filepath: The path of the file that will be used to update.
        """
        print("Updating file: ", target)
        with open(source_filepath, 'rb') as src, open(target, 'wb') as dest:
            dest.write(src.read())

    @staticmethod
    def rmdir(directory):
        """
        Recursively removes directories.
        :param directory: The path of the directory to be removed.
        """
        try:
            # List all files and subdirectories in the directory
            for filename in uos.listdir(directory):
                path = f"{directory}/{filename}"

                # Check if this is a file or a subdirectory
                if HomeUpdate.item_is_file(path):  # this is a file
                    uos.remove(path)
                else:  # this is a directory
                    HomeUpdate.rmdir(path)

            # Now that the directory is empty, remove the directory itself
            uos.rmdir(directory)
        except OSError as e:
            if e.args[0] != errno.ENOENT:
                raise
            print(f"Directory {directory} does not exist to remove")

    @staticmethod
    def makedirs(path):
        """
        Recursively creates directories.
        :param path: The path of the directory to be created.
        """
        parts = path.split('/')
        current_path = ''
        for part in parts:
            current_path += '/' + part
            try:
                os.mkdir(current_path)
            except OSError as e:
                if e.args[0] != 17:
                    raise

    def __init__(self, ftp_client: FTPClient, remote_manifest_path):
        self.ftp = ftp_client
        self.remote_manifest_path = remote_manifest_path
        self.update_dir = '/updates'
        self.makedirs(self.update_dir)
        self.can_update = False

    def _update_path(self, file):
        path = file if file.startswith("/") else f"/{file}"
        return f"{self.update_dir}{path}"

    def download_manifest(self):
        try:
            self.ftp.connect()
            self.ftp.makepasv()
            self.ftp.download_file(self.remote_manifest_path, self._update_path("manifest.json"))
            self.ftp.disconnect()
        except Exception as e:
            raise DownloadError(f"Error Downloading manifest.json: {e}")

    def open_manifest(self):
        try:
            with open(self._update_path("manifest.json"), 'r') as f:
                self.manifest = json.load(f)
        except Exception as e:
            raise UpdateError(f"Error opening manifest.json: {e}")

    def parse_manifest(self):
        if self.manifest is None:
            raise UpdateError("Must download a manifest.json file")
        files = self.manifest.get('files')
        directories = self.manifest.get("directories")
        package_root = self.manifest.get("package_root")
        self.manifest_files = files if files is not None else []
        self.manifest_directories = directories if directories is not None else []
        self.package_root = package_root if package_root is not None else ""

    def prep_update_directories(self):
        for i in self.manifest_directories:
            self.makedirs(self._update_path(i))

    def can_download(self):
        has_package_root = self.package_root is not None and self.package_root
        has_files_to_download = self.manifest_files is not None and self.manifest_files
        return has_package_root and has_files_to_download

    def download_manifest_files(self):
        try:
            self.ftp.connect()
            self.ftp.makepasv()
            for i in self.manifest_files:
                remote_path = self.package_root + i
                self.ftp.download_file(remote_path, self._update_path(i))
            self.ftp.disconnect()
        except Exception as e:
            raise DownloadError("Error downloading update: ", e)
        else:
            self.can_update = True

    def update_files(self):
        for file in uos.listdir(self.update_dir):
            if file == "manifest.json":
                continue
            if self.item_is_file(self._update_path(file)):
                self.update_file(f'/{file}', self._update_path(file))
            else:
                self.rmdir(f'/{file}')  # Remove the existing directory from root
                uos.rename(self._update_path(file), f'/{file}')

    def remove_update_directory(self):
        """
        Removes the directory where the downloaded files are stored.
        """
        self.rmdir(self.update_dir)


class UpdateManager:
    """
    UpdateManager class handles the firmware updates for the device.
    """

    def __init__(self, host, user, password, observer_func=None):
        """
        Initializes UpdateManager with provided parameters.

        :param host (str): The FTP host address.
        :param user (str): The username for the FTP host.
        :param password (str): The password for the FTP host.
        """
        self.ftp_client = FTPClient(host, user, password)
        self.observer_func = observer_func

    def observe(self, message):
        if self.observer_func is not None:
            self.observer_func(message, log_type='update')

    def download_update_from_manifest(self, remote_path):
        update = HomeUpdate(self.ftp_client, remote_path)
        update.download_manifest()
        update.open_manifest()
        update.parse_manifest()
        if not update.can_download():
            raise UpdateError("Unable to download update")
        update.prep_update_directories()
        update.download_manifest_files()
        if update.can_update:
            update.update_files()
        update.remove_update_directory()
