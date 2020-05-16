
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name = 'full_alchemyst',
    version = '0.0.1',
    description = "Les's to use a unique ORM to manage the persistence in one project. ",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author = 'Sergio Posada Urrea',
    author_email = 'sergio.posadaurrea@gmail.com',
    url = 'https://github.com/pochecho/full_alchemyst',
    packages = setuptools.find_packages(),
    download_url = 'https://github.com/pochecho/full_alchemyst.git',
    keywords = ['MongoAlchemyst', 'SqlAlchemyst', 'Flask','DB'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ],
    python_requires = ">=3.6"
)