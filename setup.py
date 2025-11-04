"""
Setup script for Swarmy package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="swarmy",
    version="1.0.0",
    author="Swarm Intelligence Research",
    description="A swarm intelligence simulation using distance-limited communication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
    ],
    extras_require={
        "visualization": ["pygame>=2.0.0"],
        "analysis": ["matplotlib>=3.3.0", "pandas>=1.1.0"],
        "dev": ["pytest>=6.0.0"],
    },
)
