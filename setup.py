#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import waliki

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = waliki.__version__

if sys.argv[-1] == 'publish':
    os.system('sudo python setup.py sdist bdist_wheel upload')
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

install_requires = ['django', 'markups', 'sh', 'docutils', 'rst2html5']


extras_require = {                                      # noqa
        'restructuredtext': [],
        'markdown': ['markdown']
    }

everything = set()
for deps in extras_require.copy().values():
    everything.update(deps)

extras_require['all'] = everything


setup(
    name='waliki',
    version=version,
    description="""An extensible wiki app for Django with a Git backend""",
    long_description=readme + '\n\n' + history,
    author=u'Martín Gaitán',
    author_email='gaitan@gmail.com',
    url='https://github.com/mgaitan/waliki',
    packages=[
        'waliki',
    ],
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    license="BSD",
    zip_safe=False,
    keywords='django wiki git waliki restructuredtext markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
