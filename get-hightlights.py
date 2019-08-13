#!/usr/bin/env python3
from typing import Optional, List, Tuple
import json
import sys
import requests


def get_all(cookie: str):
    page = 0
    items = []
    while True:
        res = requests.get(
            'https://www.blinkist.com/api/textmarkers_v2',
            params={
                'locale': 'en',
                'page'  : str(page),
                'order' : 'book',
            },
            headers={'Cookie': cookie},
        )
        res.raise_for_status()
        if res.status_code == 204:
            # no more requests needed
            break

        items.extend(res.json())
        page += 1
    return items


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--cookie', type=str, required=True)
    args = p.parse_args()

    items = get_all(cookie=args.cookie)
    json.dump(items, fp=sys.stdout, indent=2)


if __name__ == '__main__':
    main()
