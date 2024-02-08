from setuptools import setup, find_packages

setup(
    name="rdf-loader",
    author="Nataša Džudžar",
    version="0.2",
    packages=find_packages(),
    namespace_packages=["plugin", "plugin.loader"],
     entry_points={
        "plugin.loader":
        ["rdf-loader=plugin.loader.rdf_loader:RdfParser"]
    },
    install_requires=["sok-core>=0.1", "rdflib"],
    zip_safe=True
)
