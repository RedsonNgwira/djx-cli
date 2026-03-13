from setuptools import setup, find_packages

setup(
    name="djx",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["Django>=4.2,<6.0", "click>=8.0"],
    entry_points={
        "console_scripts": [
            "djx=djx.cli:cli",
        ],
    },
    author="Your Name",
    description="Convention over configuration for Django - Rails-like scaffolding and generators",
    python_requires=">=3.8",
)
