#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'Yahoo-ticker-downloader',
    license='BSD3',
    keywords = "market finance yahoo ticker stock stocks etf future futures index mutualfund currency warrant bond bonds".split(),
    description='A web scraper for ticker symbols from yahoo finance',
    packages = find_packages(),
    scripts = ['TickerDownloader.py'],
    install_requires=[
        "requests >= 2.4.3",
        "tablib >= 0.9.11",
        "backports.csv >= 1.0.4",
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: BSD License",
    ],
)

