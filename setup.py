#!/usr/bin/env python

from setuptools import setup
from Phyme import version

setup(name='Phyme',
      packages=['Phyme'],
      include_package_data=True,
      version=version,
      description='Python rhyming dictionary for songwriting',
      author='James Wenzel',
      author_email='jameswenzel@berkeley.edu',
      url='https://github.com/jameswenzel/Phyme',
      download_url=('https://github.com/jameswenzel/Phyme/tarball/' + version),
      license='MIT License',
      keywords=['songwriting', 'rhyme', 'rhyming', 'dictionary', 'slant',
                'rhymes', 'song', 'writing'],
      classifiers=[])
