from setuptools import setup, find_packages

setup(
    # naziv komponente prilikom instaliranja        ===> ovo treba instalirati u djangu u stvari
    name="sok-core",
    # verzija komponente
    version="0.1",
    namespace_packages=['core'],
    packages=find_packages(),
    install_requires=['Django>=3.1'],   #moramo imati django da bi ovo mogli instalirati
    zip_safe=False,
    package_data={'core': ['static/.css', 'static/.js', 'static/.html', 'templates/.html']} #reci mu da ukljuci iz ovih foldera ovo
)
