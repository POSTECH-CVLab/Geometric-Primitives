from setuptools import setup
import os
import sys


path_requirements = 'requirements.txt'
list_packages = ['geometric_primitives']

with open(path_requirements) as f:
    required = f.read().splitlines()

setup(
    name='geometric_primitives',
    version='0.1.0',
    author='Jungtaek Kim',
    author_email='jtkim@postech.ac.kr',
    url='https://github.com/POSTECH-CVLab/Geometric-Primitives',
    license='MIT',
    description='It is for constructing a 3D shape.',
    packages=list_packages,
    python_requires='>=3.5, <4',
    install_requires=required,
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ]
)
