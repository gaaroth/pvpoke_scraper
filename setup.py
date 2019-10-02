from setuptools import find_packages, setup

setup(
    name='pvpoke-scraper',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    zip_safe=False,
)
