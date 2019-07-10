import re
import sys
import struct
import shutil
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


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
        name='pyctp._{}'.format(k),
        language='c++',
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=[v],
        sources=['pyctp/{}.{}'.format(k, 'pyx')],
    )
    ext_modules.append(extm)
    if platform.startswith('win'):
        k = '{}.dll'.format(v)
    else:
        extm.extra_link_args = ['-Wl,-rpath,$ORIGIN']
        k = 'lib{}.so'.format(v)
    package_data.append(k)
    v = 'pyctp/{}'.format(k)
    shutil.copy2('{}/{}'.format(api_dir, k), v)

setup(
    name='pyctp',
    version=__version__,
    author=__author__,
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    packages=['pyctp'],
    package_dir={'pyctp': 'pyctp'},
    package_data={'pyctp': package_data},
)
