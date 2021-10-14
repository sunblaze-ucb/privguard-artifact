----------------------------------------------------------------

**The PrivGuard code is an academic research prototype, and meant to elucidate protocol details and for proofs-of-concept, and benchmarking. It is still under development in a production environment and is not meant for deployment currently as it only supports limited external functions.**

----------------------------------------------------------------

# PrivGuard

PrivGuard is a a proof-of-concept implementation of [PrivAnalyzer](https://wanglun1996.github.io/publication/poly19.pdf).

## Prerequisite

The statis analyzer has been tested in Ubuntu 16.04 system. To run the static analyzer, pleaes install python3.6 and python3.6-venv using the following lines.

```
sudo apt install python3.6
sudo apt install python3.6-venv
```

Then create a virtual environment for python3.6 by running

```
python3.6 -m venv venv
```

Activate the virtual environment by running

```
source path-to-venv/venv/bin/activate
```

Download the source code of the static analyzer, and run

```
path-to-repo/setup.sh
```

to install the static analyzer.

## How to use

This codebase contains (1) a policy parser to translate Legalease policy strings into Python object; (2) a set of function summaries specifying the privacy effect of commonly used data analysis functions; (3) a static analyzer that checks whether a Python program satisfies a Legalease policy.

To test the policy parser, run

```
python path-to-repo/src/parser/policy_tree.py
```

and input a valid policy string (e.g. "ALLOW FILTER age >= 18 AND SCHEMA NotPHI, h2 AND FILTER gender == 'M' ALLOW (FILTER gender == 'M' OR (FILTER gender == 'F' AND SCHEMA PHI))") in Legalease. The program will output the policy translated to Python objects.

To test converting a policy into its DNF form, run

```
python path-to-repo/src/parser/policy_tree.py
```

We provide two example programs to test the static analyzer. To run the two examples, use the following script with correct flag values. Please make sure your environment variable is correctly set before testing the below functionality (see setup.sh for more information).

```
python path-to-repo/src/analyze.py --script path-to-script --data_folder path-to-folder
``` 
