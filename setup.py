import setuptools
from setuptools import setup

setup(
    name='colstract',
    version='0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/piratecaveman/colstract',
    license='None',
    author='Pirate Caveman',
    author_email='iamrobox001@tutanota.com',
    description='colorscheme generator',
    package_data={
        '': ['examples/*', 'templates/*', 'walconfig/*']
    }
)

