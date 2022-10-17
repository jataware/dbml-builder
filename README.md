# dbml-builder
Generates Pydantic and SQLAlchemy from a DBML file.

## Usage

Install using pip:

```
pip install dbml_builder
```

Generate your ORM and schemas by running:

```
model-build generate ./project.dbml src/generated
```
or call `generate_models` directly in Python code.

You can check to if the model code is still valid by running:
```
model-build check v0.9.3 src/generated
```
or call `verify` directly in Python code.

