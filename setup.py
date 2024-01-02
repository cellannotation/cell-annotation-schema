import pathlib
from setuptools import setup, find_packages


# The directory containing this file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="cell-annotation-schema",
    version="__version__",
    # version="v0.5-beta",
    description="Cell Annotation Schema",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cellannotation/cell-annotation-schema",
    author="",
    license="Apache-2.0 license",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=("test*",)),
    include_package_data=True,
    install_requires=["jsonschema==4.4.0", "ordered-set==4.1.0", "deepmerge==1.1.0",
                      "ruamel.yaml"],
    package_data={'cas_schema': ['schemas/*.json']}
)
