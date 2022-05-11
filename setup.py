#! /usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup


setup(name="python-zetlab",
      version='0.0.4',
      description='ZetLab ADC/DAC controller module',
      url='https://github.com/RAA80/python-zetlab',
      author='Ryadno Alexey',
      author_email='aryadno@mail.ru',
      license='MIT',
      packages=['zet'],
      package_data={"zet": ["*.dll"]},
      platforms=['Windows',],
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: Microsoft :: Windows',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                  ]
     )
