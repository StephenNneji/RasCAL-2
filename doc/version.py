import os
import re

# The regex for major, minor and bugfix version, including alpha/beta/rc tags
VERSION_REGEX = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
                           r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
                           r"(?:\.(?:0|[1-9]\d*|\d *[a-zA-Z-][0-9a-zA-Z-]*))*))?"
                           r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?")


def get_doc_version():
    """Grabs doc version from environment variable"""
    doc_version = 'dev'
    version = os.environ.get('DOC_VERSION', 'dev')

    if version != 'dev':
        tmp = VERSION_REGEX.match(version.replace(' ', ''))
        if tmp is not None:
            major, minor, *other = list(tmp.groups())
            doc_version = f'{major}.{minor}'

    return doc_version
