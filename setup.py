"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""

import sys


# Allows override on the CLI by setting the --set-version=<version> option.
def get_version(default_version='0.9.0'):
    version_prefix = '--set-version='
    version_args = [arg for arg in sys.argv if arg.startswith(version_prefix)]
    if len(version_args) == 1:
        version_arg = version_args.pop()
        sys.argv.remove(version_arg)
        return version_arg.replace(version_prefix, '')
    if len(version_args) > 1:
        print(f'ERR: Multiple set-version arguments supplied: {version_args}.', file=sys.stderr)
        sys.exit(1)
    return default_version


VERSION = get_version()

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='envyconfig',
    version=VERSION,
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
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
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
