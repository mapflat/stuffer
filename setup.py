#! /usr/bin/env python3

from setuptools import setup, find_packages

requirements = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name="stuffer",
    maintainer="Lars Albertsson",
    maintainer_email="lalle@mapflat.com",
    url="http://bitbucket.org/mapflat/stuffer",
    version="0.1",
    install_requires=requirements,
    packages=find_packages(exclude=["tests"]),
    entry_points="""
      [console_scripts]
      stuffer=stuffer.main:cli
    """
)
