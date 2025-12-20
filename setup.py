from setuptools import setup, find_packages

setup(
    name="jdm_engine",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt6>=6.6.0"
    ],
    python_requires=">=3.10",
    url="https://github.com/yourusername/survey_engine",
    author="Your Name",
    description="Survey Editor Engine for PyQt6",
)
