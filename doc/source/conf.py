# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import datetime
from urllib.parse import urljoin

sys.path.insert(0, os.path.abspath(".."))

from version import get_doc_version


DOCS_PATH = os.path.abspath(os.path.dirname(__file__))
BUILD_PATH = os.path.join(DOCS_PATH, 'build', 'html')
ROOT_PATH = os.path.join(DOCS_PATH, "..", "..")

url = os.environ.get('DOC_URL', '')

project = 'RasCAL-2'
copyright = u"2024-{}, ISIS Neutron and Muon Source".format(datetime.date.today().year)
author = 'ISIS Neutron and Muon Source'
version = get_doc_version()
# The full version, including alpha/beta/rc tags.
release = version
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_title = "RasCAL-2"
html_logo = "_static/logo.png"
html_favicon = "_static/logo.png"
html_static_path = ['_static']
html_css_files = ["custom.css"]
html_copy_source = False
html_show_sourcelink = False
html_theme_options = {
    "show_prev_next": False,
    "logo": {
        "text": "RasCAL-2",
    },
    "secondary_sidebar_items": [],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/RascalSoftware/RasCAL-2",
            "icon": "fa-brands fa-github",
        },
    ],
    'navbar_start': ['navbar-logo', 'version-switcher'],
    'switcher': {'json_url': urljoin(url, 'switcher.json'),
                 'version_match': version,
                 'check_switcher': False, },
}

html_sidebars = {
    "index": [],
    "install": [],
    "example": [],
}

rst_epilog = """
.. |Angstrom| replace:: :math:`\mathring{A}`
.. |tutorial data| raw:: html

   <a href="https://indico.stfc.ac.uk/event/792/contributions/4939/attachments/1739/7049/Virtual%20Reflectometry%20School%202026.zip" target="_blank">tutorial data</a>
.. |add| image:: /images/create.png
          :scale: 10

.. |delete| image:: /images/delete.png
             :scale: 10
             
.. |options| image:: /images/settings.png
            :scale: 10
"""
