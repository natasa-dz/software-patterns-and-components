from setuptools import find_packages
from setuptools import setup

setup(
    name="complex_visualizer",
    author="Uros Muskinja",
    version="0.1",
    packages=find_packages(),
    namespace_packages=["plugin", "plugin.visualizer"],
    entry_points={
        'visualizer': ['complex_visualizer = plugin.visualizer.complex_visualizer:ComplexVisualizer']
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)
