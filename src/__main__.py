#!/usr/bin/env python3
import sys

from config.file_config import FileConfig
from media_submissions_downloader import MediaSubmissionDownloader
from service.imgur import Imgur
from service.reddit import Reddit
from service.redgif import Redgif

if __name__ == "__main__":
    file_config = FileConfig(sys.argv[1])

    reddits = [Reddit(config) for config in file_config.reddit_configs()]
    imgur = Imgur(file_config.imgur_config())
    redgif = Redgif()

    downloader = MediaSubmissionDownloader(reddits, imgur, redgif, file_config.user_agent())
    downloader.run()
