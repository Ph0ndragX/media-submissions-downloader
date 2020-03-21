#!/usr/bin/env python3

__author__ = 'Ph0ndragX'
__banner__ = 'MediaSubmissionDownloaderForReddit v1.0 by Ph0ndragX. ' \
             'This script allows you to download your saved reddit submission as media files. It can handle links ' \
             'to imgur images and albums, gfycat links and direct links to media files.'

from config.arg_config import ArgConfig
from config.config import Config
from config.file_config import FileConfig
from media_submissions_downloader_for_reddit import MediaSubmissionDownloaderForReddit
from service.imgur import Imgur
from service.reddit import Reddit
from submission.media_submissions import MediaSubmissions

if __name__ == "__main__":
    arg_config = ArgConfig(__banner__)
    file_config = FileConfig(arg_config.config_file())
    config = Config(arg_config, file_config)
    imgur = Imgur(config.imgur_credentials())
    reddit = Reddit(config.reddit_credentials())
    media_submissions = MediaSubmissions(config, reddit, imgur)
    downloader = MediaSubmissionDownloaderForReddit(config, media_submissions)
    downloader.run()
