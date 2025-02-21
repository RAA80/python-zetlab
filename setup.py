#! /usr/bin/env python3

from setuptools import setup

setup(name="python-zetlab",
      version="0.0.6",
      description="ZetLab ADC/DAC controller module",
      url='https://github.com/RAA80/python-zetlab',
      author="Alexey Ryadno",
      author_email="aryadno@mail.ru",
      license="MIT",
      packages=["zet", "zet.libs"],
      package_data={"zet": ["libs/*.dll"]},
      platforms=["Windows"],
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Science/Research",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: Microsoft :: Windows",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.9",
                   "Programming Language :: Python :: 3.10",
                   "Programming Language :: Python :: 3.11",
                  ],
     )
