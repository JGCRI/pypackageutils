from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='pypackageutils',
    version='0.1.0',
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
