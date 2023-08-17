from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="typed_graphene",
    packages=find_packages(include=["typed_graphene", "typed_graphene.*"]),
    version="0.0.4",
    description="Type-safe interface for graphene-python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jeong Yeon Nam<tonynamy@apperz.co.kr>",
    license="MIT",
    install_requires=[],
    setup_requires=["graphene>=2.0.0, <3"],
    tests_require=["pytest==7.4.0"],
    test_suite="tests",
    project_urls={
        "Source": "https://github.com/tonynamy/typed-graphene",
        "Documentation": "https://github.com/tonynamy/typed-graphene",
        "Tracker": "https://github.com/tonynamy/typed-graphene/issues",
    },
)
