from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="avri-api",
    version="0.1.7",
    description="Unofficial wrapper around Avri endpoints",
    author="Tim van Cann",
    author_email="timvancann@gmail.com",
    packages=['avri'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timvancann/pyavri",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "requests>=2.22.0",
        "pyfunctional>=1.3.0"
    ]
)
