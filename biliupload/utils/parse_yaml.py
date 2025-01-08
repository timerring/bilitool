# Copyright (c) 2025 biliupload

import yaml

def parse_yaml(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    
    # Extracting the required values
    line = data.get('line')
    streamers = data.get('streamers', {})
    
    # Assuming there's only one streamer entry
    for streamer_path, streamer_info in streamers.items():
        copyright = streamer_info.get('copyright')
        tid = streamer_info.get('tid')
        title = streamer_info.get('title')
        desc = streamer_info.get('desc')
        tags = streamer_info.get('tag')

    return line, copyright, tid, title, desc, tags

if __name__ == '__main__':
    parse_yaml('')