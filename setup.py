from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='LDScriptures',
      version='0.2.0    ',
      description='Powerful tool for getting the LDS (mormon) scriptures in your python script.',
      author='CustodiSec',
      author_email='tgb1@protonmail.com',
      url='https://github.com/tgsec/ldscriptures',
      packages=['ldscriptures'],
      include_package_data=True,
      package_data={'ldscriptures': ['ldscriptures/languages.json']},
      long_description=read('README.rst'),
      install_requires = ['bs4', 'requests', 'autodoc'], 
      keywords = ['mormon', 'lds', 'latter', 'day', 'saints', 'book of mormon', 'scriptures', 'bible', 'pearl of great price',
                  'doctrine and convenants', 'church of jesus christ', 'parse', 'citation']
     )
