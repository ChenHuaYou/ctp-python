import re
import sys
import struct
from distutils.core import setup, Extension
from Cython.Build import cythonize


api_name = 'ctpapi-se'
api_version = 'v6.3.15_20190220'
lib_quote, lib_trade = 'thostmduserapi_se', 'thosttraderapi_se'

libs = (
    ('MdApi', lib_quote),
    ('TraderApi', lib_trade),
)

with open('pyctp/__init__.py', 'r') as f:
    data = f.read()
__version__ = re.search(r"__version__ = '(.+?)'", data).group(1)
__author__ = re.search(r"__author__ = '(.+?)'", data).group(1)


def get_platform():
    map1 = {'win32': 'win', 'linux2': 'linux', 'linux': 'linux'}
    map2 = {'darwin': 'ios'}
    os = sys.platform
    if os in map1:
        return '{}{}'.format(map1[os], struct.calcsize('P')*8)
    return map2.get(os, os)


platform = get_platform()
api_dir = 'api/{name}_{version}_{platform}/lib'.format(name=api_name, version=api_version, platform=platform)
include_dirs = ['api/{name}_{version}_{platform}/include/{name}'.format(name=api_name, version=api_version, platform=platform)]
library_dirs = [api_dir]
ext_modules, package_data = [], []
for k, v in libs:
    extm = Extension(
        'pyctp._{}'.format(k),
        ['pyctp/{}.{}'.format(k, 'pyx')],
        language='c++',
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=[v],
    )
    ext_modules.append(extm)
    file_temp = '{}.dll' if platform.startswith('win') else 'lib{}.so'
    package_data.append(file_temp.format(k))

setup(
    name='pyctp',
    version=__version__,
    author=__author__,
    ext_modules=cythonize(ext_modules, language_level=2),
    packages=['pyctp'],
    package_dir={'pyctp': 'pyctp'},
    package_data={'pyctp': package_data},
)
