from setuptools import setup, find_packages

setup(
    name='Editor',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6, <4',
    install_requires=[
        'pvleopard',
        'pydub',
        'tqdm',
        'openai',
        'nltk',
        'pytest',
        'python-dotenv',
        'numpy',
        'moviepy',
        'pillow',
        'requests'
    ],
    extras_require={
        'dev': [
            'pytest>=3.7',
        ],
    },
    package_data={
        'Editor': ['Audio/audio_transcriber/leopard_params_fr.pv'],
    },
)

