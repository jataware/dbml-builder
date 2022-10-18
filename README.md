# dbml-builder

Generates Pydantic and SQLAlchemy from a DBML file.

This package is for users wanting to use their data model represented
in [DBML](https://www.dbml.org/home/) in production. `dbml-builder` accomplishes this
by:
1. Generating Pydantic and SQLAlchemy code.
2. Verifying existing generated code to see if it matches the specified version and
   has not been changed since creation.

Currently, there doesn't seem to be a good solution for code generation with DBML in Python
hence the creation of `dbml-builder`. Additionally, large software systems tend to break as
Pydantic schemas are modified which is the reason why the package includes verification
functionality.

`dbml-builder` is new and actively developed. If you have any feature requests or issues,
please submit them [here](https://github.com/jataware/dbml-builder/issues). 


## Installation

Install using pip:

```
pip install dbml_builder
```

## Usage

Generate your ORM and schemas by running:

```
model-build generate ./project.dbml ./generated
```
or call `generate_models` directly in Python code.


You can check to if the model code is still valid by running:
```
model-build check v0.9.3 ./generated
```
or call `verify` directly in Python code.

Note that the version is what is specified in the `note` for
a given project in DBML.

### Example

Suppose we have a project:

```
>> ls
src/  LICENSE  poetry.lock  data-model.dbml  pyproject.toml
```
where `src` contains your code for your python project.

We can automatically generate code using:

```
pip install dbml_builder
model-build generate ./data-model.dbml ./src/generated
```

We can now submit `src/generated` to version control and
use the generated code in a module:
```
from generated.schema import SOME_PYDANTIC_SCHEMA
from generated.orm import SOME_SQLALCHEMY_TABLE
```

We can also ensure the generated code is not changed by 
placing a check in our code:
```
# src/main.py
from dbml_builder import verify

verify('v0.1.0', '../data-model.dbml')
```
