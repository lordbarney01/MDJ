from setuptools import setup, find_packages

requirements = [
    x.strip() for x
    in open('requirements.txt').readlines() if not x.startswith('#')]

description = "This package is the celery tasks of MDJ"

setup(
    name='api',
    version="0.0.1",
    author='barney',
    author_email='noone@nowhere.com',
    url='https://github.com/lordbarney01/MDJ.git',
    description=description,
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    include_package_data=True,
)
