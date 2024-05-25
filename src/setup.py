from setuptools import setup, find_packages

# Read the contents of your requirements.txt file
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='TheoryFlashcards',
    version='1.1',
    packages=find_packages(),
    install_requires=required,
    license = "GNU GPLv3",
    author='Sachin Thakrar',
    author_email='contact@sachinthakrar.me',
    description='A project to construct flashcards for all Driving Theory Tests',
    long_description=open('../README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hoixw/TheoryFlashcards',  # Replace with your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)