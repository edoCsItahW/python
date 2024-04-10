from setuptools import setup, Extension  
from Cython.Build import cythonize  
  
extensions = [  
    Extension("systemTools", ["systemTools.py"])  
]  
  
setup(  
    name="systemTools",  
    version="0.0.9",
    description="Some tools to simplify system operations.",
    ext_modules=cythonize(extensions),  
)
