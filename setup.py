import setuptools

setuptools.setup(
    name="s3breeze",
    version="0.0.1",
    author='yevhen-m',
    description="S3Breeze",
    url="https://github.com/yevhen-m/s3breeze",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['s3breeze=s3breeze.main:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
