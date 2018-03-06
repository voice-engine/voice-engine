#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

README = \
'''
The library includes building blocks to create voice interface applications
'''


requirements = [
    # 'pyaudio'   # not included for ci
]

setup_requirements = [
    # TODO: put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest'
]

setup(
    name='voice-engine',
    version='0.0.4',
    description="Voice engine to build voice interaction applications",
    long_description=README,
    author="Yihui Xiong",
    author_email='yihui.xiong@hotmail.com',
    url='https://github.com/voice-engine/voice-engine',
    packages=find_packages(include=['voice_engine']),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
        ],
    },
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='voice doa beamforming kws',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
