# -*- coding: utf-8 -*-
from setuptools import setup
from distutils.extension import Extension
import platform
import sys
import warnings

if "--without-cseabreeze" in sys.argv:
    sys.argv.remove("--without-cseabreeze")  # this is a hack...
    # user requests to not install cython wrapper
    _extensions = []
else:
    # default to building the cython wrapper
    try:
        # try to import cython
        from Cython.Build import cythonize
    except ImportError:
        # if cython is not installed fall back to the provided C file
        cythonize = lambda x: x
        fn_ext = "c"
    else:
        fn_ext = "pyx"

    # The windows version of the cython wrapper depends on winusb
    if platform.system() == "Windows":
        libs = ['seabreeze', 'winusb']
    else:
        libs = ['seabreeze', 'usb']

    # define extension
    try:
        import numpy
    except ImportError:
        warnings.warn("Installation of cseabreeze backend requires numpy.")
        exit(1)

    extensions = [Extension('seabreeze.cseabreeze.wrapper',
                        ['./seabreeze/cseabreeze/wrapper.%s' % fn_ext],
                        include_dirs=[numpy.get_include()],
                        libraries=libs,
                      )]
    _extensions = cythonize(extensions)

setup(
    name='seabreeze',
    version='0.4.1',
    author='Andreas Poehlmann',
    author_email='mail@andreaspoehlmann.de',
    packages=['seabreeze',
              'seabreeze.cseabreeze',
              'seabreeze.pyseabreeze',
              'seabreeze.pyseabreeze.interfaces'],
    scripts=['scripts/seabreeze-compare'],
    description=('Python interface module for oceanoptics spectrometers. '
                 'This software is not associated with Ocean Optics. '
                 'Use it at your own risk.'),
    long_description=open('README.md').read(),
    requires=['python (>= 2.7)', 'pyusb (>= 1.0)', 'numpy'],
    ext_modules=_extensions,
)
