from setuptools import setup, find_packages

setup(
    name='Fiszki',
    version='4.0',
    description='Offline vocabulary learning app with spaced repetition',
    author='Wojciech Halasa',
    author_email='halasawojciech@gmail.com',
    url='https://github.com/PantoYT/Fiszki',
    
    packages=find_packages(),
    include_package_data=True,
    
    install_requires=[
        'PyMuPDF>=1.23.8',
        'requests>=2.31.0',
    ],
    
    entry_points={
        'console_scripts': [
            'fiszki=flashcard_app:main',
        ],
    },
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    
    python_requires='>=3.10',
)
