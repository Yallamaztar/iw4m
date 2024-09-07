from setuptools import setup, find_packages

setup(
    name="iw4m",
    version="0.1.0",
    description="A Python wrapper for the IW4M-Admin API",
    author="budiworld",
    author_email="budi.world@yahoo.com",
    url="https://github.com/Yallamaztar/iw4m", 
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
