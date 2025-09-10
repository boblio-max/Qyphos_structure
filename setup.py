from setuptools import setup, find_packages

setup(
    name='quantum_leap_emulator',
    version='1.0.0',
    author='Nikhil Mahankali',
    description='A high-performance, feature-rich quantum computer emulator with GPU and noise simulation support.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'matplotlib>=3.4.0',
        'scipy>=1.7.0',
        'tqdm>=4.62.0'
    ],
    extras_require={
        'gpu': ['cupy-cuda11x'] # User needs to select the correct CUDA version
    },
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
    ],
)
