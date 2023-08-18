from distutils.core import setup
from setuptools import find_packages

setup(
  name='pycw7',
  packages=find_packages(),
  version='0.0.11',
  description='Python package to simplify working with H3C Comware7 Based devices ',
  author='H3C',
  license='Apache2',
  url='https://github.com/H3C/pycw7',
  download_url='https://github.com/H3C/pycw7/tarball/0.0.9',
  classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'

    ],
  keywords='H3C Comware7 FlexFabric Netconf API ',

  package_data={'pycw7': ['utils/templates/textfsm_temps/*.tmpl']},
  install_requires=[
      'textfsm==1.1.0',
      'lxml',
      'ncclient',
      'scp',
      'ipaddr>=2.1.11',
      'paramiko'
  ],
)