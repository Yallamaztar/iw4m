from setuptools import setup, find_packages

setup(
    name="iw4m",
    version="0.1.0",
    author="budiworld",
    author_email="budi.world@yahoo.com",
    description="A Python wrapper for the IW4M-Admin API",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Yallamaztar/iw4m", 
    packages=find_packages(),
    install_requires=[
        "requests",
        "aiohttp",
        'beautifulsoup4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
