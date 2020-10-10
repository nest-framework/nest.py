"""
Created by Epic at 10/9/20
"""
from setuptools import setup, find_packages

setup(
    name='nest.py',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/nest-framework',
    license='MIT',
    author='Epic',
    description='A simple discord bot framework using speedcord',
    install_requires=[
        "speedcord",
        "click",
        "ujson",
        "aiohttp",
        "tqdm"
    ],
    entry_points={
        "console_scripts": [
            "nest=nest.__main__:main"
        ]
    }
)
