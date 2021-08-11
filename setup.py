import re
from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()

def get_requirements():
    """Return a list of package requirements from the requirements.txt file."""
    with open('requirements.txt') as f:
        return f.read().split()
        
version = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", open('pypackageutils/__init__.py').read(), re.M).group(1)

setup(
    name='pypackageutils',
    version=version,
    packages=find_packages(),
    url='https://github.com/JGCRI/pypackageutils.git',
    license='BSD 2-Clause',
    author='Chris R. Vernon',
    author_email='chris.vernon@pnnl.gov',
    description='Common utilities used in Python modeling software packages',
    long_description=readme(),
    long_description_content_type="text/markdown",
    python_requires='>=3.6.*, <4',
    install_requires=[
        "requests~=2.20.0",
        "pandas~=1.2.4"
    ],
    include_package_data=True
)
