from os import remove
from setuptools import find_packages, setup
from typing import List



HYPHON_E_DOT="-e ."


# Function to get requirments ( file  ) . we have given file path in string. return -> list
def get_requirements(filepath: str) -> List[str]:
    requirements=[]

    # here we are opening requirements as an object files and reading  
    with open(filepath) as file_obj:
        requirements=file_obj.readlines()
        requirements=[i.replace("\n","") for i in requirements] # in (python) requirements, when we enter there is hidden text ( \n ) indicating next line 
                                                                 # we are simply replacing it with blank 

        # -e . this is used to create the intial setup
        if HYPHON_E_DOT in requirements:
            requirements.remove(HYPHON_E_DOT) # we want this to run only for. first time 

# We create setup file to show the project info and its version 
setup(
    name='Machine_Learning_Project',
    vesion='0.0.1',
    description=' Machine Learning Pipeline Project',
    author='Kaustubh Gidh',
    author_email='kaustubhgidh06_gmail.com',
    url='',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)