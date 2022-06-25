import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
    
setuptools.setup(
    name="git-timewarp",
    version="0.0.1",
    author="Michael Arcidiacono",
    author_email="",
    description="time travel to a previous git commit",
    long_description="", #long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mixarcid/git-timewarp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[]
)
