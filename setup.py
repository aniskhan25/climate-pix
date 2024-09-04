from setuptools import setup, find_packages

setup(
    name='climatepix',
    version='0.1.0',
    description='A tool for fetching environmental indicators for coordinates.',
    author='@nis',
    author_email='aniskhan25@gmail.com',
    url='https://github.com/aniskhan25/climatepix',
    license="GPLv3+",

    packages=find_packages(where='climatepix'),
    package_dir={'': 'climatepix'},

    install_requires=[
        'pandas',
        'rasterio',
        'fiona',
    ],

    python_requires='>=3.6',
)