from setuptools import setup, Extension  
from Cython.Build import cythonize  
  
extensions = [  
    Extension("sqlTools", ["sqlTools.py"])  
]  
  
setup(  
    name="sqlTools",  
    version="0.0.1",
    description="sqlTools",
    ext_modules=cythonize(extensions),  
)