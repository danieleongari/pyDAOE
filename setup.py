#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

if __name__ == '__main__':
    setup(packages=find_packages(),
          long_description=LONG_DESCRIPTION,
          long_description_content_type='text/markdown',
          name="pyDAOE",
          author="Daniele Ongari",
          author_email="daniele.ongari@gmail.com",
          description="Design and Analysis of Experiments",
          url="https://github.com/danieleongari/pyDAOE",
          license="Creative Commons",
          classifiers=["Programming Language :: Python"],
          version="0.1.0",
          install_requires=["numpy", "scipy", "pandas", "matplotlib"],
          extras_require={
              "testing": ["pytest==6.2.5", "pytest-cov==2.12.1"],
              "pre-commit": [
                  "pre-commit==2.15.0",
                  "yapf==0.31.0",
                  "prospector==1.5.1",
              ]
          })
