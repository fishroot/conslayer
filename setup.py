#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setuptools based installation."""

__author__ = 'Patrick Michl'
__email__ = 'patrick.michl@gmail.com'
__license__ = 'MIT'
__docformat__ = 'google'

import re
from pathlib import Path
import setuptools
from setuptools.command.install import install as Installer

# Module Constants
AUTHOR = 'Patrick Michl'
PKGNAME = 'conslayer'

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

    # Install package
    setuptools.setup(
        name=PKGNAME,
        version=pkg_vars['version'],
        description=pkg_vars['description'],
        long_description=Path('.', 'README.md').read_text(),
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Games/Entertainment',
            'Operating System :: OS Independent',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3'],
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
        python_requires='>=3.7',
        install_requires=[
            'reactivex>=4.0',
        ],
        entry_points={
            'console_scripts': [
                'conslayer = conslayer:main']},
        zip_safe=True)

if __name__ == '__main__':
    install()