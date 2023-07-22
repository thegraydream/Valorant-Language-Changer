# Version
VERSION = "1.0.0"
import os
import requests
import json

if not os.path.exists('theme.json'):open('theme.json', 'w', encoding='utf-8').write(requests.get('https://raw.githubusercontent.com/thegraydream/Valorant-Language-Changer/master/theme.json').text)

# Import
import subprocess
import json
import threading
import shutil
import time
import customtkinter
customtkinter.set_default_color_theme("theme.json")
from tkinter import filedialog, messagebox
import psutil


# Application Data
class application:
    data = None

    def get_data():
        try:
            application.data = json.loads(requests.get('https://raw.githubusercontent.com/thegraydream/Valorant-Language-Changer/master/application.json').text)
        except:
            application.data = open('application.json', 'r', encoding='utf-8').read()

    def get(data):
        try:
            if application.data == None:application.get_data()
            return json.loads(application.data)[data]
        except Exception as e:log.error(e)

# Riot Data
class riot_data:
    data = None

    def get_data():
        try:
            if riot_data.data == None:riot_data.data = json.loads(requests.get('https://clientconfig.rpg.riotgames.com/api/v1/config/public?namespace=keystone.products.valorant.patchlines').text)
            return riot_data.data
        except Exception as e:log.error(e) 



# Log
class log:
    def error(text):
        print(f'ERROR: {text}')
        messagebox.showerror(application.get('name'), f"An error has occurred, please contact an administrator on the discord link on the github: https://github.com/thegraydream/Valorant-Language-Changer\n\nError: {text}")
        quit()

    def ok(text):
        print(f'OK: {text}')


# Checking File
def check_file():
    if not os.path.exists('config.json'):open('config.json', 'w', encoding='utf-8').write(requests.get('https://raw.githubusercontent.com/thegraydream/Valorant-Language-Changer/master/config.json').text)
    if not os.path.exists('icon.ico'):open('icon.ico', 'wb', encoding='utf-8').write(requests.get('https://raw.githubusercontent.com/thegraydream/Valorant-Language-Changer/master/icon.ico').content)


# Manifest Downloader
def download_ManifestDownloader():
    try:
        log.ok('Checking ManifestDownloader.exe...')
        if os.path.exists('ManifestDownloader.exe'):
            log.ok('ManifestDownloader.exe already exists!')
            return True

        response = requests.get(application.get('manifest'), allow_redirects=True)
        open('ManifestDownloader.exe', 'wb').write(response.content)
        log.ok('ManifestDownloader.exe has been downloaded successfully!')
        return True
    except Exception as e:
        log.error(e)
        return False


# Download language
def download_language(language, type):
    if download_ManifestDownloader() == False:return
    try:
        manifest_downloader_file = 'ManifestDownloader.exe'
        base_url = 'https://valorant.secure.dyn.riotcdn.net/channels/public/bundles'
        file_pattern = f'.+{type}-WindowsClient.+'

        command = [
            manifest_downloader_file,
            riot_data.get_data()['keystone.products.valorant.patchlines.live']['platforms']['win']['configurations'][0]['patch_url'],
            '-b', base_url,
            '-l', language,
            '-o', f'lang/',
            '-f', file_pattern
        ]

        process = subprocess.run(command, shell=True, check=True)
    except Exception as e:
        log.error(e)


# Get running apllications
def get_running_applications():
    try:
        running_applications = []
        for proc in psutil.process_iter(['name']):
            try:
                process_name = proc.info['name']
                running_applications.append(process_name)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return running_applications
    except Exception as e:
        log.error(e)


# running applications for %s
def running_applications(application, times):
    try:
        for i in range(0, int(times)):
            if application in get_running_applications():
                return True
            time.sleep(1)
        return False
    except Exception as e:
        log.error(e)


# Get config and set
class config:
    try:
        def read(value=None):
            if value is None:
                return json.loads(open('config.json', 'r', encoding='utf-8').read())
            else:return config.read()[value]
    except Exception as e:
        log.error(e)

    def set(key, new_value):
        try:
            with open('config.json', 'r') as json_file:
                data = json.load(json_file)

            if key in data:
                data[key] = new_value

            with open('config.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)
            log.ok(f'Set new value in config.json "{key}" = "{new_value}"')
        except Exception as e:
            log.error(e)


# Get default choice 
def default(default_data, data):
    try:
        if not default_data in data:
            return data
        other_continents = [c for c in data if c != default_data]
        return [default_data] + other_continents
    except Exception as e:
        log.error(e)


# Check if valorant path is good
def check_valorant_path():
    try:
        if not os.path.exists(f'{config.read("valorant_path")}\live'):
            while True:
                valorant_path = filedialog.askdirectory(title='Please select the Valorant folder')
                if os.path.exists(f'{valorant_path}\live'):
                    config.set('valorant_path', valorant_path)
                    break
                messagebox.showerror(application.get('name'), "The path to the Valorant folder is invalid. Please try again.")
        log.ok(f'Valorant path is good!')
        return True
    except Exception as e:
        log.error(e)
        return False

# Check if riot path is good
def check_riot_path():
    try:
        if not os.path.exists(f'{config.read("riot_path")}\Riot Client\RiotClientServices.exe'):
            while True:
                riot_path = filedialog.askdirectory(title='Please select the Riot Games folder')
                if os.path.exists(f'{riot_path}\Riot Client\RiotClientServices.exe'):
                    config.set('riot_path', riot_path)
                    break
                messagebox.showerror(application.get('name'), "The path to the Riot Games folder is invalid. Please try again.")
        log.ok(f'Riot game path is good!')
        return True
    except Exception as e:
        log.error(e)
        return False


# Remove File Method
def remove_file(path):
    try:
        os.remove(path)
        log.ok(f'remove file {path}')
    except Exception as e:
        log.error(e)

# Copy File Method
def copy_file(path0, path1):
    try:
        shutil.copy2(path0, path1)
        log.ok(f'copy file {path0} > {path1}')
    except Exception as e:
        log.error(e)


# Application
class App(customtkinter.CTk):
    def __init__(self):
        try:
            super().__init__()

            data_language = riot_data.get_data()

            voice_language = default(config.read('voice_language'), [data for data in data_language['keystone.products.valorant.patchlines.live']['platforms']['win']['configurations'][0]['locale_data']['available_locales']])
            text_language = default(config.read('text_language'), [data for data in data_language['keystone.products.valorant.patchlines.live']['platforms']['win']['configurations'][0]['locale_data']['available_locales']])
            self.geometry("800x225")
            self.resizable(False, False)
            self.title(application.get('name'))
            self.iconbitmap('icon.ico')

            self.frame = customtkinter.CTkFrame(self, width=600, height=400, corner_radius=20)
            self.frame.pack(pady=20, padx=100, fill="both", expand=True)

            self.language_frame = customtkinter.CTkFrame(self.frame, corner_radius=20)
            self.language_frame.pack(pady=20, padx=20, fill="x")

            self.voice_language_label = customtkinter.CTkLabel(master=self.language_frame, text="Select your voice language")
            self.voice_language_label.grid(row=0, column=1, padx=100, pady=10)

            self.voice_language_menu = customtkinter.CTkOptionMenu(dynamic_resizing=False, values=voice_language, master=self.language_frame)
            self.voice_language_menu.grid(row=0, column=2, padx=10, pady=10)

            self.text_language_label = customtkinter.CTkLabel(master=self.language_frame, text="Select your text language")
            self.text_language_label.grid(row=1, column=1, padx=10, pady=10)

            self.text_language_menu = customtkinter.CTkOptionMenu(dynamic_resizing=False, values=text_language, master=self.language_frame)
            self.text_language_menu.grid(row=1, column=2, padx=10, pady=10)

            self.launch_button = customtkinter.CTkButton(master=self.frame, text="Launch Game", command=self.launch_game)
            self.launch_button.pack(side="top")

            self.info_label = customtkinter.CTkLabel(master=self, text=f"By {application.get('author')} | Version {application.get('version')}")
            self.info_label.pack(side="left", padx=5)
        except Exception as e:
            log.error(e)
    

    # Launch Game Button CallBack
    def launch_game(self):
        try:
            if "VALORANT.exe" in get_running_applications():
                messagebox.showerror(application.get('name'), f"To perform this action, please close valorant.")
                return

            if check_valorant_path() == False:return
            if check_riot_path() == False:return
            if not os.path.exists(f"{config.read('valorant_path')}/live/ShooterGame/Content/Paks/{self.voice_language_menu.get()}_Audio-WindowsClient.pak"):
                messagebox.showerror(application.get('name'), f"To set your game audio to {self.voice_language_menu.get()}, you need to change the language of your game to {self.voice_language_menu.get()}!")
                return

            threading.Thread(target=self.game_changer).start()
        except Exception as e:
            log.error(e)

    # Game modifier (Language)
    def game_changer(self):
        try:
            # Disable Button
            self.launch_button.configure(state="disabled")

            log.ok(f'Download/Verify {self.text_language_menu.get()} language')
            download_language(language=self.text_language_menu.get(), type='Text')

            log.ok('Valorant is launching!')
            command = f'start "" "{config.read("riot_path")}/Riot Client/RiotClientServices.exe" --launch-product=valorant --launch-patchline=live'
            process = subprocess.Popen(command, shell=True)

            if running_applications("VALORANT.exe", 60) == True:
                log.ok('Text files are being copied...')
                remove_file(f'{config.read("valorant_path")}/live/ShooterGame/Content/Paks/{self.voice_language_menu.get()}_Text-WindowsClient.pak')
                remove_file(f'{config.read("valorant_path")}/live/ShooterGame/Content/Paks/{self.voice_language_menu.get()}_Text-WindowsClient.sig')
                copy_file(f'lang\ShooterGame\Content\Paks\{self.text_language_menu.get()}_Text-WindowsClient.pak', f'{config.read("valorant_path")}/live/ShooterGame/Content/Paks/{self.voice_language_menu.get()}_Text-WindowsClient.pak')
                copy_file(f'lang\ShooterGame\Content\Paks\{self.text_language_menu.get()}_Text-WindowsClient.sig', f'{config.read("valorant_path")}/live/ShooterGame/Content/Paks/{self.voice_language_menu.get()}_Text-WindowsClient.sig')
                config.set('voice_language', self.voice_language_menu.get())
                config.set('text_language', self.text_language_menu.get())
                log.ok('The text files have been copied!')

            else:
                messagebox.showerror(application.get('name'), f"You didn't launch valorant in time! Please try again.")
            self.launch_button.configure(state="normal")
        except Exception as e:
            log.error(e)


if __name__ == "__main__":
    try:
        if VERSION != application.get('version'):messagebox.showinfo(application.get('name'), f"You don't have the latest version of '{application.get('name')}'! We recommend using the latest version ({application.get('version')}), your current version ({VERSION}).\n\nGithub link : {application.get('github')}")
        check_file()
        download_ManifestDownloader()
        app = App()
        app.mainloop()
    except Exception as e:
        log.error(e)
