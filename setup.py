from distutils.core import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='LDScriptures',
    version='1.0.0',
    description='Powerful tool for getting the LDS (mormon) scriptures in your python script.',
    author='CustodiSec',
    author_email='tgb1@protonmail.com',
    url='https://github.com/gabbarreiro/ldscriptures',
    packages=['ldscriptures'],
    package_data = {'ldscriptures': ['ldscriptures/languages.json']},
    data_files = [['ldscriptures', ['README.rst']]],
    long_description=read('README.rst'),
    requires = ['bs4', 'requests', 'autodoc', 'cachetools'], 
    keywords = ['mormon', 'lds', 'latter', 'day', 'saints', 'book of mormon', 'scriptures', 'bible', 'pearl of great price',
                'doctrine and convenants', 'church of jesus christ', 'parse', 'citation', 'scriptures'],
    install_requires= [
        'requests',
        'bs4'
    ]    
    )
