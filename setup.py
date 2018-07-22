from setuptools import setup

setup(name='LDScriptures',
      version='0.1.1',
      description='Powerful tool for getting the LDS (mormon) scriptures in your python script.',
      author='CustodiSec',
      author_email='tgb1@protonmail.com',
      url='https://github.com/tgsec/ldscriptures',
      packages=['ldscriptures'],
      install_requires = ['bs4', 'requests'], 
      keywords = ['mormon', 'lds', 'latter', 'day', 'saints', 'book of mormon', 'scriptures', 'bible', 'pearl of great price',
                  'doctrine and convenants', 'church of jesus christ', 'parse', 'citation']
     )
