import os
from setuptools import setup, find_packages


with open('README.md', 'r') as fh:
	LONG_DESCRIPTION = fh.read()


# All the pip dependencies required for installation.
INSTALL_REQUIRES = [
	'adventurelib==1.2',
	'marshmallow==2.18.1',
    'pymaybe==0.1.6',
	'colorama==0.4.1',
    'windows-curses ; platform_system=="Windows"',
    'pyreadline ; platform_system=="Windows"',
]


def params():

	name = "An Adventure"

	version = "0.0.2"

	description = "A text based adventure game"

	long_description = LONG_DESCRIPTION
	long_description_content_type = "text/markdown"

	install_requires = INSTALL_REQUIRES

	# https://pypi.org/pypi?%3Aaction=list_classifiers
	classifiers = [
		"Development Status :: 1 - Planning",
		"Environment :: Console :: Curses",
		"Intended Audience :: End Users/Desktop",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: Implementation :: CPython",
		"Topic :: Communications :: Chat",
		"Topic :: Games/Entertainment"
	]
	author = 'Kyle Baron, Benjamin Jacobs'
	url = 'https://github.com/ttocsneb/an_Adventure'

	packages = ['an_adventure']

	entry_points = {
		'console_scripts': [
			'anAdventure = an_adventure.__main__:main'
		]
	}

	return locals()


setup(**params())