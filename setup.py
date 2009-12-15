from setuptools import setup, find_packages

setup(
    name = "PyPalm",
    version = "0.1",
    packages = find_packages(),

    author = "Martin Grund",
    author_email = "grundprinzip@gmail.com",
    description = "PyPalm should ease handling the development of Palm WebOs applications",

    entry_points = {
        'console_scripts': [
            'pypalm = pypalm.pypalm:main_func',
            ]
        },
    
    )
