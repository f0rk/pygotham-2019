from setuptools import setup


setup(
    name="pygotham_2019",
    version="1.0",
    description="Advanced SQL with SQLAlchemy Examples",
    author="Ryan P. Kelly",
    author_email="rpkelly22@gmail.com",
    url="https://github.com/f0rk/pygotham-2019",
    install_requires=[
        "faker",
        "psycopg2",
        "sqlalchemy",
        "tabulate",
    ],
    package_dir={"": "code"},
    packages=["pygotham_2019"],
    include_package_data=True,
    zip_safe=False,
)
