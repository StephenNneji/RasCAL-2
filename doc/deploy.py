import json
import os
import shutil
import sys
from urllib.parse import urljoin

sys.path.insert(0, os.path.abspath(".."))

from rascal2 import RASCAL2_VERSION


DOCS_PATH = os.path.abspath(os.path.dirname(__file__))
BUILD_PATH = os.path.join(DOCS_PATH, 'build', 'html')
ROOT_PATH = os.path.join(DOCS_PATH, "..", "..")

url = os.environ.get('DOC_URL', '')
version = str(RASCAL2_VERSION)
if len(sys.argv) > 1 and sys.argv[1].strip().endswith(version):
    doc_version = version
else:
    doc_version = "dev"
WEB_PATH = os.path.join(ROOT_PATH, "web", doc_version)

if os.path.isdir(WEB_PATH):
    shutil.rmtree(WEB_PATH, ignore_errors=True)

shutil.copytree(BUILD_PATH, WEB_PATH, ignore=shutil.ignore_patterns('.buildinfo', 'objects.inv', '.doctrees',
                                                                    '_sphinx_design_static'))

releases = [entry.name for entry in os.scandir(os.path.join(ROOT_PATH, "web")) if
            entry.is_dir() and entry.name != '.git']
releases.sort()
switch_list = []
for release in releases:
    switch_list.append({'name': release,
                        'version': release,
                        'url': urljoin(url, release)})

SWITCHER_FILE = os.path.join(os.path.join(ROOT_PATH, "web", 'switcher.json'))
with open(SWITCHER_FILE, 'w') as switcher_file:
    json.dump(switch_list, switcher_file)

INDEX_FILE = os.path.join(os.path.join(ROOT_PATH, "web", 'index.html'))

is_latest = (len(releases) > 1 and releases[-2] == doc_version)
base_url = urljoin(url, f'{doc_version}/')
index_url = urljoin(base_url, 'index.html')
if not os.path.exists(INDEX_FILE) or is_latest:
    data = [
        '<!DOCTYPE html>\n',
        '<html>\n',
        '  <head>\n',
        f'    <title>Redirecting to {base_url}</title>\n',
        '    <meta charset="utf-8">\n',
        f'    <meta http-equiv="refresh" content="0; URL={index_url}">\n',
        f'    <link rel="canonical" href="{index_url}">\n',
        '  </head>\n',
        '</html>',
    ]

    with open(INDEX_FILE, 'w') as index_file:
        index_file.writelines(data)
