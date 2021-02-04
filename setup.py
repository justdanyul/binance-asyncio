import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="binance-asyncio", 
    version="0.0.1",
    author="Daniel Kirkegaard Mouritsen",
    author_email="daniel.mouritsen@gmail.com",
    description="Library for interacting with the Binance API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justdanyul/binance-asyncio",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'websockets',
        'aiohttp',
    ],
    python_requires='>=3.6',
)
