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
from funcy import compose, identity

"""
Issue: All of the fields in the Enum end with a comma when rendering DDL with
       PyDBML. `simple-ddl-parser` can't handle this and will just ignore the
       entire enum model and not create the model
"""
patch_trailing_commas = lambda text: text.replace(',\n)', '\n)')

"""
Issue: The final models generate models with a `blob` type instead of a `sa.LargeBinary` or `bytes` type.
"""
patch_blob_for_schema = lambda text: text.replace('blob', 'bytes')
patch_blob_for_orm = lambda text: text.replace('blob', 'sa.LargeBinary')

"""
Issue: When a default value is set to null, the model creation defaults to `NULL` which
       is uninstantiated variable in Python, so the type has to be set to NULL.
"""
patch_uppercase = lambda text: text.replace('NULL', 'null')

"""
Enhancement: Pydantic models don't make the primary keys optional which is makes it difficult to create
             new models in the API.
"""
make_ids_optional = lambda text: text.replace('id: int', 'id: Optional[int] = None')

### Bundle patches ###

"""
Patch DDL string before processing by O! My Models
"""
patch_ddl = compose(
    patch_trailing_commas, 
)

"""
Patch generated Pydantic code
"""
patch_schema = compose(
    patch_blob_for_schema, 
    patch_uppercase,
    make_ids_optional
)

"""
Patch generated ORM code
"""
patch_orm = compose(
    patch_blob_for_orm
)
