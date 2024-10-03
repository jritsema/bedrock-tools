from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='bedrock-tools',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='John Ritsema',
    author_email='john_ritsema@yahoo.com',
    description='A small Python library that simplifies Amazon Bedrock Converse API function calling (i.e., tool use).',
    keywords='ai genai bedrock tools function-calling',
    url='https://github.com/jritsema/bedrock-tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    long_description=long_description,
    long_description_content_type="text/markdown",
)