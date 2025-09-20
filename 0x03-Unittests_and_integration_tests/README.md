#!/usr/bin/env python3
Utils Unit Testing

This project contains unit tests for the `access_nested_map` function in the `utils` module.  
The tests are implemented using the **unittest** framework and the **parameterized** library to ensure correctness across multiple scenarios.

---

## Requirements

- All files are interpreted/compiled on **Ubuntu 18.04 LTS** using **Python 3.7**.
- All files must end with a new line.
- The first line of all Python files must be exactly:
  ```bash
  #!/usr/bin/env python3
A README.md file is mandatory at the root of the project folder.

Code must follow pycodestyle (version 2.5).

All files must be executable.

All modules, classes, and functions must contain proper documentation strings.

All functions and methods must include type annotations.

Project Structure
Copy code
.
├── utils.py
├── test_utils.py
├── README.md
utils.py → Contains the implementation of access_nested_map.

test_utils.py → Contains the unit tests for access_nested_map.

README.md → This file.

access_nested_map
The function access_nested_map retrieves values from a nested dictionary using a sequence of keys.

Example
python
Copy code
from utils import access_nested_map

nested_map = {"a": {"b": 2}}
result = access_nested_map(nested_map, ("a", "b"))
print(result)  # Output: 2
Unit Tests
The tests are implemented in test_utils.py using unittest and parameterized.

Tested Cases:
nested_map={"a": 1}, path=("a",) → returns 1

nested_map={"a": {"b": 2}}, path=("a",) → returns {"b": 2}

nested_map={"a": {"b": 2}}, path=("a", "b") → returns 2

Run Tests
bash
Copy code
chmod +x test_utils.py
./test_utils.py
or

bash
Copy code
python3 -m unittest test_utils.py
Documentation
Each file, class, and function contains docstrings explaining their purpose:

Module docstring explains what the file does.

Class docstring explains the role of the test class.

Function docstring explains the purpose of the function and its expected behavior.

Style
All code follows PEP 8 style guidelines (pycodestyle 2.5).
You can verify by running:

bash
Copy code
pycodestyle test_utils.py utils.py
Author
Project developed for practicing Python unit testing, parameterized testing, and code quality best practices.

yaml
Copy code

---

✅ This README includes:
- System requirements  
- Style and docstring requirements  
- Project structure  
- Example usage of `access_nested_map`  
- Instructions for running tests  

Would you like me to also **add docstrings + type annotations** into the actual `uti
