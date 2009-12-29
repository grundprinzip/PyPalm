from setuptools import setup, find_packages
import pypalm.pypalm as pp

setup(
    name = "PyPalm",
    version = pp.VERSION,
    packages = find_packages(),

    author = "Martin Grund",
    author_email = "grundprinzip@gmail.com",
    description = "PyPalm should ease handling the development of Palm WebOs applications",

    url = "http://github.com/grundprinzip/PyPalm",
    
    entry_points = {
        'console_scripts': [
            'pypalm = pypalm.pypalm:main_func',
            ]
        },
    
    )
