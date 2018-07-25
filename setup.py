#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

requirements = [
    # 'pyaudio'   # not included for ci
]


test_requirements = [
    'pytest'
]

setup(
    name='voice-engine',
    version='0.1.3',
    description="Voice engine to build voice enabled applications",
    long_description=long_description,
    long_description_content_type='text/markdown',
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
    tests_require=test_requirements
)
