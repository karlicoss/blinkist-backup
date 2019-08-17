#!/usr/bin/env python3
import argparse
from typing import Optional, List, Tuple, Dict
import json
import sys
import requests

def get_library(*, cookies):
    # apparently returns all at once and pagination isn't necessary??
    return requests.get(
        'https://www.blinkist.com/api/books/library',
        cookies=cookies,
    ).json()['entries']

def get_highlights(*, cookies):
    page = 0
    items: List[Dict] = []
    while True:
        res = requests.get(
            'https://www.blinkist.com/api/textmarkers_v2',
            params={
                'page'  : str(page),
                'order' : 'book',
            },
            cookies=cookies,
        )
        res.raise_for_status()
        if res.status_code == 204:
            # no more requests needed
            break
        rj = res.json()
        items.extend(rj)
        page += 1
    return items



# ugh, seems that meta contains only similar books. not sure where is title coming from...
# def get_metas(*, cookie: str, ids: List[str]):
#     requests.get(
#         'https://api.blinkist.com/v4/books/metas',
#         headers={'Cookie': cookie},
#     )


def main():
    cname = '_blinkist-webapp_session'
    p = argparse.ArgumentParser()
    p.add_argument('--cookie', type=str, required=True, help=f'Value for {cname} cookie (see https://stackoverflow.com/a/10015468/706389)')
    args = p.parse_args()

    cookies = {
        cname: args.cookie,
    }

    books      = get_library(cookies=cookies)
    highlights = get_highlights(cookies=cookies)
    json.dump({
        'books'     : books,
        'highlights': highlights,
    }, fp=sys.stdout, indent=2)


if __name__ == '__main__':
    main()
