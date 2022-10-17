"""
fix.py - The generation of the ORMs and schemas relies on two libraries 'PyDBML' and
         'O! My Models'. Both of these packages are mildly brittle so the DDL generated
         by 'PyDBML' needs to be massaged so the 'simple-ddl-parser' (the dependency of
         'O! My Models' that parses DDL) will not crash.

         The primary export of this library is `patch` which takes a string of DDL text
         and patches it so the `create_models` function won't break on the parsing step.

         Hopefully, patches will be submitted upstream so this module can be dropped.
         Upstream PRs and fixes will also be provided in the comment below.
"""
from funcy import compose

"""
Issue: All of the fields in the Enum end with a comma when rendering DDL with
       PyDBML. `simple-ddl-parser` can't handle this and will just ignore the
       entire enum model and not create the model
"""
patch_trailing_commas = lambda text: text.replace(',\n)', '\n)')

"""
Issue: The final models generate models with a `blob` type instead of a `str` type.
       This obviously throws an error because `blob`s are not a valid type in Python.
"""
patch_nomenclature = lambda text: text.replace('blob', 'varchar')

"""
Issue: When a default value is set to null, the model creation defaults to `NULL` which
       is uninstantiated variable in Python, so the type has to be set to NULL.
"""
patch_uppercase = lambda text: text.replace('NULL', 'null')


patch = compose(
    patch_trailing_commas, 
    patch_nomenclature, 
    patch_uppercase
)
