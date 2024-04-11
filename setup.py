#!/usr/bin/env python3
# -*-coding:Utf-8 -*


# To install the package, run :  ` pip install -e . `

import setuptools
import codecs


CLASSIFIERS = [
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Scientific/Engineering :: Visualization",
    "Operating System :: Unix",
    "Operating System :: MacOS",
]

NAME = "sshicstuff"

MAJOR = 1
MINOR = 0
MAINTENANCE = 0
VERSION = "{}.{}.{}".format(MAJOR, MINOR, MAINTENANCE)

LICENSE = "GPLv3"
AUTHOR = "Nicolas Mendiboure, Loqmen Anani"
AUTHOR_EMAIL = "nicolas.mendiboure@ens-lyon.fr"
URL = "https://github.com/nmendiboure/ssHiCstuff"

with codecs.open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().splitlines()


setuptools.setup(
    name=NAME,
    version=VERSION,
    description="A package to ananlyze the data generated by Hi-C Capture for ssDNA, extension of HiCstuff package",
    long_description=LONG_DESCRIPTION,
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    classifiers=CLASSIFIERS,
    packages=setuptools.find_packages(),
    install_requires=REQUIREMENTS,
    include_package_data=True
)
