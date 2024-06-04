import requests
import os
import datetime
import glob

class ZoomClient:
    def __init__(self, account_id, client_id, client_secret) -> None:
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        data = {
            "grant_type": "account_credentials",
            "account_id": self.account_id,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post("https://zoom.us/oauth/token", data=data)
        return response.json()["access_token"]


    def get_recordings(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        url = "https://api.zoom.us/v2/users/me/recordings"

        return requests.get(url, headers).json()


    def get_download_url(self, meeting_id):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        url = f"https://api.zoom.us/v2/meetings/{meeting_id}/recordings"

        r = requests.get(url, headers=headers).json()

        url = [i["download_url"] for i in r['recording_files'] 
        if i['recording_type'] == 'audio_only'][0]
        download_link = f'{url}?access_token={self.access_token}&playback_access_token={r['password']}'

        return download_link


class ZoomApp:
    def __init__(self, client, **add_ons) -> None:
        self.client = client
        self.add_ons = add_ons

        # for add-ons like the artificial inteligence and the transcriber
        for key, value in add_ons.items():
            setattr(self, key, value)


    def __getitem__(self, key):
        
        if key == 'client':
            return getattr(self, key)
        
        elif key in self.add_ons:
            return self.add_ons[key]

        else:
            raise KeyError(f"'{key}' not found")


    def get_local_path(self):
        # Default directory paths where Zoom recordings might be stored
        default_paths = [
            os.path.join(os.path.expanduser("~"), "Documents", "Zoom"),
            os.path.join(os.path.expanduser("~"), "Zoom"),
        ]

        for path in default_paths:
            if os.path.exists(path):
                return path

        return None


    def get_newest_folder(self):
        folders = []
        for entry in os.scandir(self.get_local_path()):
            if entry.is_dir():
                folder_path = entry.path  # Get the full path of the folder
                folder_time = os.path.getmtime(folder_path)  # Get modification time
                folders.append((folder_time, folder_path))

        if not folders:
            return None

        newest_folder = max(folders, key=lambda x: x[0])[1]  # Get only the path
        return newest_folder


    def get_latest_mp4_file(self, directory):
        mp4_files = glob.glob(os.path.join(directory, "*.mp4"))
        if mp4_files:
            latest_mp4_file = max(mp4_files, key=os.path.getmtime)
            return latest_mp4_file
        else:
            return None


    def run(self):
        
        recs = self.client.get_recordings()
        print(recs)
        try:
            rec_id= recs["meetings"][0]['id']
            my_url = self["client"].get_download_url(rec_id)
            transcript = self['transcriber'].transcribe(my_url)
            print(transcript.text)
            with open("transcript.txt", "w") as f:
                f.write(transcript.txt)

        except Exception as e:
            print("No meetings to transcribe.")

        try:
            zoom_directory = self.get_newest_folder()
            latest_mp4_file = self.get_latest_mp4_file(zoom_directory)
            if latest_mp4_file:
                print("Latest MP4 file found:", latest_mp4_file)
                # Now you can do further processing with the MP4 file
            else:
               print("No MP4 files found in Zoom recordings directory.")
            transcript = self['transcriber'].transcribe(latest_mp4_file)
            print(transcript.text)
        except:
            print("No zoom found")