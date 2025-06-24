from setuptools import setup, find_packages

setup(
    name="griem",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
        "scipy",
        "tabulate"
    ],
    author="Jordan Mindrup",
    description="Stark broadening calculation package using Griem theory",
    long_description = open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Cassegrain10/Stark_Broadening-Griem",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
