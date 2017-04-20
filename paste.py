#!/usr/bin/env python3
import requests
import os
from urllib.parse import urlparse


class PastesError(Exception):
    pass


def upload(path, url, title='', description='', token=''):
    with open(path, 'rb') as file:
        r = requests.post(
                url,
                data={'title': title, 'description': description, 'token': token},
                files={'file': file})
        if r.status_code != 200:
            raise PastesError(str(r.json()['errors']))
        else:
            p = urlparse(url)
            return "%s://%s%s" % (p.scheme, p.netloc, r.json()['url'])


if __name__ == "__main__":
    import configparser
    import argparse

    parser = argparse.ArgumentParser(description="Upload a file to a django-pastes server")
    parser.add_argument("file", type=str, help="The file to upload")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser('~'), '.pastes'))
    print(upload(args.file, config['pastes']['url'], token=config['pastes']['token']))
