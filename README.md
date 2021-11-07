# PyDAOE: Design and Analysis of Experiments

Based on the book [Design and Analysis of Experiments](https://www.wiley.com/en-us/Design+and+Analysis+of+Experiments%2C+10th+Edition-p-9781119492443) by Douglas C. Montgomery,
which is covered by the [Design of Experiments Specialization](https://www.coursera.org/specializations/design-experiments) on Coursera, taught by Prof. Montgomery himself.

Note that you can freely attend all the lectures as an auditor, and each "week" of lecture covers 
exactly one chapter of the book (12 in total, splitted into 4 courses).

You can also browse a summary of the DoE concepts as [notes of the STAT 503 course at Penn State University](https://online.stat.psu.edu/stat503/home).

After downloading and installing the package as
```
git clone https://github.com/danieleongari/pyDAOE.git
cd pyDAOE
pip install -e .
```
one can find the examples and exercises inspired from the book in the `tests` directory.
In the case of examples/exercises that are exploiting exclusively external packages
or that use visual representation of the results,
they are solved in the Jupyter Notebooks in the `notebooks` directory. 

The reference version of the book uses imperial units, and specifically the 9th edition of the book, 
which is also used as a reference in the Coursera specialization.

One can also install directly the last stable version as
```
pip install pydaoe
```
and copy&paste data and examples in your Jupyter Notebook.

## Dependencies

This repository rely on other great packages:
- `pandas` - used as the main format for inputs and outputs
- [`pyDOE2`](https://github.com/clicumu/pyDOE2) - based on the dormient project 
[`pyDOE`](https://github.com/tisimst/pyDOE), it contains many utilities to design experiments, but not much for their
analysis
- [`statsmodels`](https://www.statsmodels.org/stable/index.html) - originaly built upon `scipy.stats`, it contains
lots of advanced features for the analysis of experiments
- `scipy` - contains some basic tools which are also used by `statsmodel`, e.g., the functions of distributions

## Development
```
git clone https://github.com/danieleongari/pyDAOE.git
cd pyDAOE
pip install -e .[testing,pre-commit]
pre-commit install
```