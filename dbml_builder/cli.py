"""
cli.py - This script wraps the packages functionality in a CLI interface
"""

from click import argument, echo, group

from dbml_builder.build import generate_models, verify

@group()
def main() -> None:
    """
    Manage the data store API service
    """
    pass


@main.command()
@argument('version', nargs=1)
@argument('path_to_generated_dir', nargs=1)
def check(version: str, path_to_generated_dir: str) -> None:
    """
    Verify if model code matches current DBML version
    """
    is_success, message = verify(version, path_to_generated_dir)
    if is_success:
        echo('Version match! Generated model code is up to date.')
    else:
        echo(f'Verification failed because {message}.')
        
@main.command()
@argument('path_to_dbml', nargs=1)
@argument('path_to_generated_dir', nargs=1)
def generate(path_to_dbml: str, path_to_generated_dir: str) -> None:
    """
    Generate model code

    `gen` should only be called when developing using a new version of the DBML.
    """
    generate_models(path_to_dbml, path_to_generated_dir)
    echo('Generated pydantic schemas')


if __name__ == "__main__":
    main()
