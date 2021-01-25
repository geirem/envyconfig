"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='envyconfig',
    version='1.0.1',
    description='YAML reader with ENV interpolation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/geirem/envyconfig',
    author='https://github.com/geirem',
    author_email='geiremb@gmail.com',
    classifiers=[
        # https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='configtools development',
    package_dir={'': 'envyconfig'},
    packages=find_packages(where='envyconfig'),
    python_requires='>=3.8',
    extras_require={
        'test': ['pytest'],
        'googlesecrets': ["google-cloud-secret-manager"]
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/geirem/envyconfig/issues',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/geirem/envyconfig/',
    },
)
