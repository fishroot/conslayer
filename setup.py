#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setuptools based installation."""

__author__ = 'Patrick Michl'
__email__ = 'patrick.michl@gmail.com'
__license__ = 'GPLv3'
__docformat__ = 'google'

import os
import re
import sys
from pathlib import Path
import setuptools
from setuptools.command.install import install as Installer

# Module Constants
AUTHOR = 'Patrick Michl'
PKGNAME = 'conslayer'

# class CustomInstaller(Installer):
#     """Customized setuptools install command."""

#     def run(self) -> None:
#         """Run installer."""
#         Installer.run(self)
#         # Run post installation script
#         # import subprocess
#         # subprocess.call([sys.executable, __file__, 'postinstall'])

def get_vars() -> dict:
    """Get __VAR__ module variables from package __init__ file."""
    text = Path(PKGNAME, '__init__.py').read_text()
    rekey = "__([a-zA-Z][a-zA-Z0-9_]*)__"
    reval = r"['\"]([^'\"]*)['\"]"
    pattern = f"^[ ]*{rekey}[ ]*=[ ]*{reval}"
    dvars = {}
    for match in re.finditer(pattern, text, re.M):
        dvars[str(match.group(1))] = str(match.group(2))
    return dvars

def install() -> None:
    """Setuptools based installation script."""
    # Update package variables from package init
    pkg_vars = get_vars()

    # Install nemoa package
    setuptools.setup(
        name=PKGNAME,
        version=pkg_vars['version'],
        description=pkg_vars['description'],
        long_description=Path('.', 'README.md').read_text(),
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering',
            'Operating System :: OS Independent',
            'License :: OSI Approved :: GPLv3',
            'Programming Language :: Python :: 3',
    		'Programming Language :: Python :: 3.8'],
        keywords=(
            "game "
            "console "),
        author=pkg_vars['author'],
        author_email=pkg_vars['email'],
        license=pkg_vars['license'],
        packages=setuptools.find_packages(),
        package_dir={
            PKGNAME: PKGNAME},
        cmdclass={
            'install': Installer},
        python_requires='>=3.8',
        install_requires=[],
        entry_points={
            'console_scripts': [
                'conslayer = conslayer:main']},
        zip_safe=False)

# def post_install() -> None:
#     """Post installation script."""
#     import appdirs
#     def copytree(src: str, tgt: str) -> None:
#         import glob
#         import shutil
#         print(f"copying {src} -> {tgt}")
#         for srcsdir in glob.glob(os.path.join(src, '*')):
#             tgtsdir = os.path.join(tgt, os.path.basename(srcsdir))
#             if os.path.exists(tgtsdir):
#                 shutil.rmtree(tgtsdir)
#             try:
#                 shutil.copytree(srcsdir, tgtsdir)
#             except shutil.Error as err: # unknown error
#                 print(f"directory not copied: {str(err)}")
#             except OSError as err: # directory doesn't exist
#                 print(f"directory not copied: {str(err)}")

#     print('running postinstall')

#     # copy user workspaces
#     user_src_base = str(Path('.', 'data', 'user'))
#     user_tgt_base = appdirs.user_data_dir(
#         appname=PKGNAME, appauthor=AUTHOR)
#     user_tgt_base = str(Path(user_tgt_base, 'workspaces'))
#     copytree(user_src_base, user_tgt_base)

#     # copy site workspaces
#     site_src_base = str(Path('.', 'data', 'site'))
#     site_tgt_base = appdirs.site_data_dir(
#         appname=PKGNAME, appauthor=AUTHOR)
#     site_tgt_base = str(Path(site_tgt_base, 'workspaces'))
#     copytree(site_src_base, site_tgt_base)

if __name__ == '__main__':
    # if len(sys.argv) > 1 and sys.argv[1] == 'postinstall':
    #     post_install()
    # else:
    install()