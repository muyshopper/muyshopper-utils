import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="muyshopper",
    version="0.0.1",
    author="MuyShopper",
    author_email="hola@muyshopper.com",
    description="MuyShopper utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/awolfmann/mmuu-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
