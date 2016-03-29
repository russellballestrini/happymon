# installation: pip install botoform
from setuptools import (
  setup,
  find_packages,
)

# read requirements.txt for requires, filter comments and newlines.
sanitize = lambda x : not x.startswith('#') and not x.startswith('\n')
with open('requirements.txt', 'r') as f:
    requires = filter(sanitize, f.readlines())

setup( 
    name = 'happymon',
    version = '0.0.1',
    description = 'happymon: monitoring with YAML',
    keywords = 'happymon: monitoring with YAML',
    long_description = open('README.rst').read(),

    author = 'Russell Ballestrini',
    author_email = 'russell@ballestrini.net',
    url = 'https://github.com/russellballestrini/happymon',

    packages = find_packages(),

    install_requires = requires,
    entry_points = {
      'happymon.collectors' : [
        'http = happymon.collectors:http',
      ],
      'happymon.handlers' : [
        'http_code = happymon.handlers:http_code',
      ],
      'happymon.error_handlers' : [
        'http_code = happymon.handlers:http_code_err',
      ],
      'console_scripts': [
        'hm = happymon.__main__:main',
      ],
    },
    classifiers=[
        'Intended Audience :: Operators, Developers, System Engineers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: 3.4',
    ],
)
