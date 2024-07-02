from setuptools import find_packages, setup

VERSION = "0.2"

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="mention",
    version=VERSION,
    packages=find_packages(),
    # scripts=['mention.py', 'utils.py', 'exceptions.py'],
    # metadata to display on PyPI
    author="Xolani Mazibuko",
    author_email="mazi76erx@gmail.com",
    url="https://github.com/mazi76erX2/mention-python",
    keywords="mention api examples",
    description="A Python wrapper around the Mention API.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=["requests", "requests_oauth2>=0.3.0"],
    project_urls={
        "Coverage": "https://codecov.io/gh/mazi76erX2/mention-python",
        "Documentation": "https://mention-python.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/mazi76erX2/mention-python",
    },
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
