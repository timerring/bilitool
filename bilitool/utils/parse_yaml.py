# Copyright (c) 2025 bilitool

import yaml


def parse_yaml(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # Assuming there's only one streamer entry
    copyright = data.get("copyright")
    tid = data.get("tid")
    title = data.get("title")
    desc = data.get("desc")
    tag = data.get("tag")
    source = data.get("source")
    cover = data.get("cover")
    dynamic = data.get("dynamic")
    return copyright, tid, title, desc, tag, source, cover, dynamic


if __name__ == "__main__":
    res = parse_yaml("")
    print(res)
