from distutils.core import setup
from distutils.extension import Extension
try:
    from Cython.Distutils import build_ext
    ext = 'pyx'; cmdclass = {'build_ext': build_ext}
except ImportError:
    ext = 'cpp'; cmdclass = {}
import re, sys, os, struct, shutil
fp = open('pyctp/__init__.py', 'rb'); data = fp.read(); fp.close()
if sys.version_info[0] >= 3: data = data.decode('utf-8')
__version__ = re.search(r"__version__ = '(.+?)'", data).group(1)
__author__ = re.search(r"__author__ = '(.+?)'", data).group(1)


api_name = 'ctpapi-se'
api_version = 'v6.3.15_20190220'
lib_quote, lib_trade = 'thostmduserapi_se', 'thosttraderapi_se'

BUILD = (
    ('MdApi', lib_quote),
    ('TraderApi', lib_trade),
)

def platform():
    map1 = {'win32':'win', 'linux2':'linux', 'linux':'linux'}
    map2 = {'darwin':'ios'}
    os = sys.platform
    if os in map1:
        return '%s%d' % (map1[os], struct.calcsize('P')*8)
    return map2.get(os, os)
platform = platform()

api_dir = 'api/{name}_{version}_{platform}/lib'.format(name=api_name, version=api_version, platform=platform)
include_dirs = ['api/{name}_{version}_{platform}/include/{name}'.format(name=api_name, version=api_version, platform=platform)]
library_dirs = [api_dir]
ext_modules = []; package_data = []
for k,v in BUILD:
    extm = Extension(name='pyctp._'+k, language='c++',
        include_dirs=include_dirs, library_dirs=library_dirs,
        libraries=[v], sources=['pyctp/%s.%s'%(k,ext)],
    )
    ext_modules.append(extm)
    if platform.startswith('win'):
        k = '%s.dll'%v
    else:
        extm.extra_link_args = ['-Wl,-rpath,$ORIGIN']
        k = 'lib%s.so'%v
    package_data.append(k)
    v = 'pyctp/' + k
    shutil.copy2('%s/%s'%(api_dir,k), v)

setup(
    name='pyctp', version=__version__, author=__author__,
    cmdclass=cmdclass, ext_modules=ext_modules,
    packages=['pyctp'], package_dir={'pyctp':'pyctp'}, package_data={'pyctp':package_data},
)
