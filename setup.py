__author__ = 'shako'
from setuptools import setup, find_packages

# dependencies
with open('requirements.txt') as f:
    deps = f.read().splitlines()

version = "0.1.0"

# main setup script
setup(
    name="powerDataRaptorUploader",
    version=version,
    description="power data upload to raptor tool",
    author="Mozilla Taiwan",
    author_email="tw-qa@mozilla.com",
    license="MPL",
    install_requires=deps,
    packages=find_packages(),
    entry_points={'console_scripts': ['gogopower = powerDataRaptorUploader.uploader:main']},
    include_package_data=True,
    zip_safe=False
)
