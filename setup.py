from setuptools import setup, find_packages

setup(
    name='Editor',
    version='0.1',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[
        'pvleopard',
        'pydub',
        'tqdm',
        'openai',
        'nltk',
        'pytest',

        'python-dotenv',
    ],
    extras_require={
        'dev': [
            'pytest>=3.7',
        ],
    },
)
