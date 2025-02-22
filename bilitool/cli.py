# Copyright (c) 2025 bilitool

import argparse
import sys
import os
import logging
from bilitool.controller.login_controller import LoginController
from bilitool.controller.upload_controller import UploadController
from bilitool.controller.download_controller import DownloadController
from bilitool.controller.feed_controller import FeedController
from bilitool.utils.get_ip_info import IPInfo
from bilitool.utils.check_format import CheckFormat

def cli():
    logging.basicConfig(
        format='[%(levelname)s] - [%(asctime)s %(name)s] - %(message)s',
        level=logging.INFO
    )
    parser = argparse.ArgumentParser(description='The Python toolkit package and cli designed for interaction with Bilibili')
    parser.add_argument('-V', '--version', action='version', version='bilitool 0.1.2', help='Print version information')

    subparsers = parser.add_subparsers(dest='subcommand', help='Subcommands')

    # Login subcommand
    login_parser = subparsers.add_parser('login', help='Login and save the cookie')
    login_parser.add_argument('--export', action='store_true', help='(default is false) Export the login cookie file')

    # Logout subcommand
    logout_parser = subparsers.add_parser('logout', help='Logout the current account')

    # Upload subcommand
    upload_parser = subparsers.add_parser('upload', help='Upload the video')
    upload_parser.add_argument('video_path', help='(required) The path to video file')
    upload_parser.add_argument('-y', '--yaml', default='', help='The path to yaml file(if yaml file is provided, the arguments below will be ignored)')
    upload_parser.add_argument('--copyright', type=int, default=2, help='(default is 2) 1 for original, 2 for reprint')
    upload_parser.add_argument('--title', default='', help='(default is video name) The title of video')
    upload_parser.add_argument('--desc', default='', help='(default is empty) The description of video')
    upload_parser.add_argument('--tid', type=int, default=138, help='(default is 138) For more info to the type id, refer to https://biliup.github.io/tid-ref.html')
    upload_parser.add_argument('--tag', default='bilitool', help='(default is bilitool) Video tags, separated by comma')
    upload_parser.add_argument('--line', default='bda2', help='(default is bda2) Line refer to https://biliup.github.io/upload-systems-analysis.html')
    upload_parser.add_argument('--source', default='来源于网络', help='(default is 来源于网络) The source of video (if your video is re-print)')
    upload_parser.add_argument('--cover', default='', help='(default is empty) The cover of video (if you want to customize, set it as the path to your cover image)')
    upload_parser.add_argument('--dynamic', default='', help='(default is empty) The dynamic information')

    # Check login subcommand
    check_login_parser = subparsers.add_parser('check', help='Check if the user is logged in')

    # Download subcommand
    download_parser = subparsers.add_parser('download', help='Download the video')

    download_parser.add_argument('vid', help='(required) the bvid or avid of video')
    download_parser.add_argument('--danmaku', action='store_true', help='(default is false) download the danmaku of video')
    download_parser.add_argument('--quality', type=int, default=64, help='(default is 64) the resolution of video')
    download_parser.add_argument('--chunksize', type=int, default=1024, help='(default is 1024) the chunk size of video')
    download_parser.add_argument('--multiple', action='store_true', help='(default is false) download the multiple videos if have set')

    # List subcommand
    list_parser = subparsers.add_parser('list', help='Get the uploaded video list')
    list_parser.add_argument('--size', type=int, default=20, help='(default is 20) the size of video list')
    list_parser.add_argument('--status', default='pubed,not_pubed,is_pubing', help='(default is all) the status of video list: pubed, not_pubed, is_pubing')

    # Show subcommand
    show_parser = subparsers.add_parser('show', help='Show the video detailed info')
    show_parser.add_argument('vid', help='The avid or bvid of the video')

    # Convert subcommand
    convert_parser = subparsers.add_parser('convert', help='Convert between avid and bvid')
    convert_parser.add_argument('vid', help='The avid or bvid of the video')

    # IP subcommand
    ip_parser = subparsers.add_parser('ip', help='Get the ip info')
    ip_parser.add_argument('--ip', default='', help='(default is your request ip) The ip address')

    args = parser.parse_args()

    # Check if no subcommand is provided
    if args.subcommand is None:
        print("No subcommand provided. Please specify a subcommand.")
        parser.print_help()
        sys.exit()

    if args.subcommand == 'login':
        LoginController().login_bilibili(args.export)

    if args.subcommand == 'logout':
        LoginController().logout_bilibili()

    if args.subcommand == 'check':
        LoginController().check_bilibili_login()

    if args.subcommand == 'upload':
        # print(args)
        UploadController().upload_video_entry(args.video_path, args.yaml, args.line, 
        args.copyright, args.tid, args.title, args.desc, args.tag, args.source, args.cover, args.dynamic)

    if args.subcommand == 'download':
        # print(args)
        DownloadController().download_video_entry(args.vid, args.danmaku, args.quality, args.chunksize, args.multiple)
    
    if args.subcommand == 'list':
        FeedController().print_video_list_info(args.size, args.status)
    
    if args.subcommand == 'show':
        FeedController().print_video_info(args.vid)

    if args.subcommand == 'convert':
        CheckFormat().convert_bv_and_av(args.vid)
    
    if args.subcommand == 'ip':
        IPInfo.get_ip_address(args.ip)

if __name__ == '__main__':
    cli()