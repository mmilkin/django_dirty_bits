from setuptools import setup


setup(
    name='django_dirty_bits',
    version='0.1',
    description=open('README.rst').read(),
    author='Michael Milkin',
    author_email='mmilkin@gmail.com',
    py_modules=['django_dirty_bits'],
    install_requires=['django'],
)
