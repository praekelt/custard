from setuptools import setup

import re


def listify(filename):
    return filter(None, open(filename, 'r').read().split('\n'))

setup(
    name="custard",
    version="0.0.1",
    url='http://github.com/praekelt/custard',
    license='BSD',
    description="Utilities for talking to a GSM modem over a Telnet protocol",
    long_description=open('README.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    packages=[
        "custard",
        "twisted.plugins",
    ],
    package_data={
        'twisted.plugins': ['twisted/plugins/custard_plugin.py'],
    },
    include_package_data=True,
    install_requires=listify('requirements.txt'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Framework :: Twisted',
    ],
)
