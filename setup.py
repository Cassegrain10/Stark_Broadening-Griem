from setuptools import setup, find_packages
from pathlib import Path

# Load dependencies from requirements.txt
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = requirements_path.read_text(encoding="utf-8").splitlines()

setup(
    name="griem",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    author="Jordan Mindrup",
    description="Stark broadening calculation package using Griem theory",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/Cassegrain10/Stark_Broadening-Griem",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
