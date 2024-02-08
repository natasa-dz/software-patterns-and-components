from setuptools import setup, find_packages

setup(
    name="xml-loader",
    author="Damjanov Dusan",
    version="0.1",
    packages=find_packages(),
    namespace_packages=["plugin", "plugin.xml_loader"],

    entry_points={
        "loader":
        ["xml-loader=plugin.xml_loader.loader:XMLLoader"]
    },
    install_requires=["sok-core>=0.1"],
    zip_safe=True
)