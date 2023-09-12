# HOW TO USE THE `generate_sound_pack.py` SCRIPT

1. Install the `yt-dlp` library using the command `pip install yt-dlp`
2. Install `ffmpeg` on your computer and make sure it is added to your `PATH`
3. Create a `sound.json` file with the following format:

```json
{
  "sound": {
    "codename_1": {
      "url": "url_to_mp3_file_or_youtube_1"
    },
    ...
    "codename_n": {
      "url": "url_to_mp3_file_or_youtube_n"
    }
  }
}
```

4. Run the `generate_sound_pack.py` script

NB: The script supports both direct URLs to MP3 files or YouTube URLs
