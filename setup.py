import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hrmtools",
    version="0.0.1",
    author="Christopher Ulmschneider",
    author_email="ulmschneider.chris@gmail.com",
    description="hrmtools for plotting and data handling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["pysimplegui",
                      "pandas",
                      "matplotlib",
                      "numpy"],
    url="https://github.com/chris-ulmy/hrmtools.git",
    packages=["hrmtools"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
