import sys
import os
from setuptools import setup

if sys.version_info[0] == 2:
    raise ValueError('This package requires Python 3.7 or newer')
elif sys.version_info[0] == 3:
    if not sys.version_info >= (3, 7):
        raise ValueError('This package requires Python 3.7 or newer')
else:
    raise ValueError('Unrecognized major version of Python')

# Read version
version_globals = {}
with open(os.path.join("nttt", "_version.py")) as fp:
    exec(fp.read(), version_globals)

__project__ = 'nttt'
__desc__ = 'A utility for Nina to clean up translated projects'
__version__ = version_globals['__version__']
__author__ = "Martin O'Hanlon"
__author_email__ = 'martin.ohanlon@raspberrypi.org'
__url__ = 'https://github.com/raspberrypilearning/nttt'

if __name__ == '__main__':
    setup(name='nttt',
          version = __version__,
          description = __desc__,
          url = __url__,
          author = __author__,
          author_email = __author_email__,
          packages = [__project__],
          entry_points={
              'console_scripts': [
                  'nttt = nttt:main'
              ]},
          zip_safe=False)
