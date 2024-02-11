import os
import ftplib


class FTPUploader:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.ftp = None
        self.excluded_files = []
        self.uploaded_files = []
        self.uploaded_directories = []

    def set_excluded_files(self, excluded):
        self.excluded_files = excluded

    def connect(self):
        self.ftp = ftplib.FTP()
        self.ftp.connect(self.host)
        self.ftp.login(self.user, self.password)

    def change_directory(self, path):
        self.ftp.cwd(path)

    def create_directory(self, path):
        try:
            self.ftp.mkd(path)
        except ftplib.error_perm:
            pass  # Directory already exists

    def upload_file(self, local_file, remote_file):
        with open(local_file, "rb") as f:
            self.ftp.storbinary(f"STOR {remote_file}", f)

    def disconnect(self):
        self.ftp.quit()
        self.ftp = None

    def upload_folder(self, local_folder, remote_folder):
        for item in os.listdir(local_folder):
            if item == '.DS_Store' or item in self.excluded_files:
                continue
            local_path = os.path.join(local_folder, item)
            remote_path = f"{remote_folder}/{item}"

            if os.path.isfile(local_path):
                self.uploaded_files.append(remote_path)
                self.connect()
                self.upload_file(local_path, remote_path)
                print(f'\tuploaded: {item}')
                self.disconnect()

            elif os.path.isdir(local_path):
                self.uploaded_directories.append(remote_path)
                self.connect()
                self.create_directory(remote_path)
                self.disconnect()
                self.upload_folder(local_path, remote_path)

    def clear_folder(self, folder):
        if self.ftp is None:
            self.connect()
        items = self.ftp.nlst(folder)
        for item in items:
            try:
                self.change_directory(item)  # Try changing directory, if it's a directory it will succeed
                self.change_directory('..')  # Go back up to the parent directory
                self.clear_folder(item)  # Recursively clear the subdirectory
                self.ftp.rmd(item)  # Remove the subdirectory
            except ftplib.error_perm:
                self.ftp.delete(item)  # If it's a file, delete it
