from setuptools import find_packages, setup

setup(
    name="TherapyTalk-Chatbot-using-Llama2",
    version="0.0.1",
    author="Md Oazed Uddin",
    author_email="oazedlium@gmail.com",
    find_packages=find_packages(), # Find packages will be looking fo constructor(__init__) file in each folder and where it will get that file it will be considered as a package
    install_requires=[],
)