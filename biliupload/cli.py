# Copyright (c) 2025 biliupload

import argparse
import sys
import os
import logging
from biliupload.login.login_bili import login_bili
from biliupload.utils.parse_cookies import parse_cookies
from biliupload.upload.bili_upload import BiliUploader
from biliupload.utils.parse_yaml import parse_yaml

def cli():
    logging.basicConfig(
        format='[%(levelname)s] - [%(asctime)s %(name)s] - %(message)s',
        level=logging.INFO
    )
    parser = argparse.ArgumentParser(description='Python implementation of biliup')
    parser.add_argument('-V', '--version', action='version', version='biliupload 1.0', help='Print version information')

    subparsers = parser.add_subparsers(dest='subcommand', help='Subcommands')

    # Login subcommand
    subparsers.add_parser('login', help='login and save the cookies')

    # Upload subcommand
    upload_parser = subparsers.add_parser('upload', help='upload the video')
    upload_parser.add_argument('video_path', help='(required) the path to video file')
    upload_parser.add_argument('-c', '--cookies', required=True, help='The path to cookies')
    upload_parser.add_argument('-y', '--yaml', help='The path to yaml file(if yaml file is provided, the arguments below will be ignored)')
    upload_parser.add_argument('--copyright', type=int, default=2, help='(default is 2) 1 for original, 2 for reprint')
    upload_parser.add_argument('--title', help='(default is video name) The title of video')
    upload_parser.add_argument('--desc', default='', help='(default is empty) The description of video')
    upload_parser.add_argument('--tid', type=int, help='(default is 138) For more info to the type id, refer to https://biliup.github.io/tid-ref.html')
    upload_parser.add_argument('--tags', help='(default is biliupload) video tags, separated by comma')
    upload_parser.add_argument('--line', default='bda2', help='(default is bda2) line refer to https://biliup.github.io/upload-systems-analysis.html')

    args = parser.parse_args()

    # Check if no subcommand is provided
    if args.subcommand is None:
        print("No subcommand provided. Please specify a subcommand.")
        parser.print_help()
        sys.exit()

    if args.subcommand == 'login':
        login_bili()

    if args.subcommand == 'upload':
        sessdata, bili_jct = parse_cookies(args.cookies)
        if (args.yaml):
            line, copyright, tid, title, desc, tags = parse_yaml(args.yaml)
            BiliUploader(
                sessdata,
                bili_jct,
                line
            ).upload_and_publish_video(
                args.video_path,
                title=title,
                desc=desc,
                copyright=copyright,
                tid=tid,
                tags=tags
            )
        else:
            BiliUploader(
                sessdata,
                bili_jct,
                args.line
            ).upload_and_publish_video(
                args.video_path,
                title=args.title,
                desc=args.desc,
                copyright=args.copyright,
                tid=args.tid,
                tags=args.tags
            )

if __name__ == '__main__':
    cli()