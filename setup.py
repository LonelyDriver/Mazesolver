import setuptools

#with open("README.md", "r", encoding="utf-8") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="mazesolver-pkg-LonelyDriver", # Replace with your own username
    version="0.0.1",
    author="Maximilian Rickers",
    author_email="max_rickers@hotmail.de",
    description="Shows the shortest way out of a maze",
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        
    ]
)