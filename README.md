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

Download the source code of the static analyzer by running

```
git clone https://github.com/sunblaze-ucb/privguard-artifact.git
```

Then enter the root directory of the repo, and create and activate a python3.6 virtual environment, install python packages, and set environment variables by running

```
chmod u+x ./setup.sh
./setup.sh
```

## How to use

This codebase contains (1) a policy parser to translate Legalease policy strings into Python object; (2) a set of function summaries specifying the privacy effect of commonly used data analysis functions; (3) a static analyzer that checks whether a Python program satisfies a Legalease policy.

To test the policy parser, run

```
python path-to-repo/src/parser/policy_parser.py
```

and input a valid policy string (e.g. "ALLOW FILTER age >= 18 AND SCHEMA NotPHI, h2 AND FILTER gender == 'M' ALLOW (FILTER gender == 'M' OR (FILTER gender == 'F' AND SCHEMA PHI))") in Legalease. The program will output the policy translated to Python objects.

To test converting a policy into its DNF form, run

```
python path-to-repo/src/parser/policy_tree.py
```

## Example Test Cases

We are still actively cleaning up the example programs and corresponding function summaries. We currently provide 5 example programs (0, 4, 5, 6, 23) to test the static analyzer. To run the examples, use the following script with correct flag values. Please make sure your environment variable is correctly set before testing the below functionality (see setup.sh for more information).

```
python path-to-repo/src/analyze.py --example_id 4
```

## Code structure

The code is organized into three sub-directories under `src` directory: (1) `parser` which contains the parser and implementation of PrivGuard policies; (2) `stub_libraries` which contains the implementation of function summaries; (3) `examples` which contains the example programs and corresponding policies.

The organization of the `parser directory` is as below.

```
            policy_tree.py
                 |
           policy_parser.py
           /           \
abstract_domain.py     attribute.py
      |
typed_value.py
```

typed_value.py defines the basic values types (e.g. integers, strings) used in the policy. abstract_domain.py defines the corresponding lattice built on top of the defined values. attribute.py defines the attributes in the policy. policy_parser.py is the real parser that converts the policy strings into lists of basic tokens. policy_tree.py further organizes the tokens in a tree structure convenient for analysis.
