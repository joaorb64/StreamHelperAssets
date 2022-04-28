import json, youtube_dl, requests, shutil, time, os
from pathlib import Path

directory = "./sound"
url_json_path = "./url.json"
with open(url_json_path, 'rt', encoding="utf-8") as url_json_file:
    url_dict = json.loads(url_json_file.read()).get("sound")

def robust_request(link, timeout=30):
    return_code = 404
    while return_code != 200:
        try:
            response = requests.get(link, timeout=timeout)
            return_code = response.status_code
        except requests.exceptions.ConnectionError:
            return robust_request(link)
    return response

def download_from_youtube(url, filename, directory, retries=0):
    ydl_options = {
        'noplaylist': True,
        'format': 'bestaudio/best',
        'outtmpl': f'{directory}/{filename}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        try:
            ydl.download([url])
        except youtube_dl.utils.DownloadError:
            if retries < 10:
                time.sleep(1)
                print(f"Retrying download of {filename}.mp3")
                download_from_youtube(url, filename, directory, retries=retries+1)
            else:
                raise

def download_from_direct_url(url, filename, directory):
    print("Downloading from direct URL...")
    mp3_filename = f"{filename}.mp3"
    with open(f"{directory}/{mp3_filename}", "wb") as mp3_file:
        response = robust_request(url)
        mp3_file.write(response.content)

def generate_config(directory):
    config_dict = {
        "name": "Sound",
        "description": "Character themes",
        "prefix": "sound_",
        "postfix": "_",
        "type": ["sound"],
        "credits": "",
        "version": "1.0"
    }

    config_contents = json.dumps(config_dict, indent=2)
    with open(f"{directory}/config.json", "wt", encoding="utf-8") as config_file:
        config_file.write(config_contents)

if os.path.exists(directory):
    shutil.rmtree(directory)
Path(directory).mkdir(parents=True, exist_ok=True)

for codename in url_dict.keys():
    url = url_dict[codename].get("url")
    print(f"Processing character {codename}")
    filename = f"sound_{codename}_0"
    if url:
        if "youtube.com" in url or "youtu.be" in url:
            download_from_youtube(url, filename, directory)
        else:
            download_from_direct_url(url, filename, directory)
    alt_versions = url_dict[codename].get("alt")
    if alt_versions:
        for index in alt_versions.keys():
            filename = f"sound_{codename}_{index}"
            url = alt_versions[index]
            if url:
                if "youtube.com" in url or "youtu.be" in url:
                    download_from_youtube(url, filename, directory)
                else:
                    download_from_direct_url(url, filename, directory)

generate_config(directory)

print("Download complete!")
