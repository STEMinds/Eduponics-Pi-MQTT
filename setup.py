import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eduponics-mqtt-STEMinds", # Replace with your own username
    version="0.0.1",
    author="Roni Gorodetsky",
    author_email="contact@steminds.com",
    description="Python MQTT package for STEMinds Eduponics react-native mobile app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/STEMinds/Eduponics-Pi-MQTT",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyqrcode',
        'paho-mqtt',
        'pypng'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
