from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='LDScriptures',
      version='0.3.1',
      description='Powerful tool for getting the LDS (mormon) scriptures in your python script.',
      author='CustodiSec',
      author_email='tgb1@protonmail.com',
      url='https://github.com/tgsec/ldscriptures',
      packages=['ldscriptures'],
      long_description=read('README.rst'),
      install_requires = ['bs4', 'requests', 'autodoc', 'cachetools'], 
      keywords = ['mormon', 'lds', 'latter', 'day', 'saints', 'book of mormon', 'scriptures', 'bible', 'pearl of great price',
                  'doctrine and convenants', 'church of jesus christ', 'parse', 'citation']
     )
