from setuptools import setup, find_packages

setup(
    name='climatepix',                       # The name of your package
    version='0.1.0',                          # The version of your package
    packages=find_packages(),                 # Automatically find all packages
    package_dir={'climatepix': 'climatepix'}, # Map package name to the directory
    entry_points={
        'console_scripts': [
            'climate-pix=climatepix.main:main',  # Command-line script to run main()
        ],
    },
    install_requires=[
        'pandas',
        'rasterio',
        'fiona',
        'pyproj',
    ],
    python_requires='>=3.6',                  # Specify the minimum Python version
)
