from setuptools import setup, find_packages

# Read the contents of your requirements.txt file
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='TheoryFlashcards',
    version='1.0',
    packages=find_packages(),
    install_requires=required,
    author='Sachin Thakrar',
    author_email='contact@sachinthakrar.me',
    description='A project to construct flashcards for all Driving Theory Tests',
    long_description=open('../README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hoixw/TheoryFlashcards',  # Replace with your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
       'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)