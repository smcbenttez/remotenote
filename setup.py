import setuptools  # type: ignore

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="remotenote",
    version="0.1.0",
    author="Salvador McBenttez",
    author_email="salvador.mcbenttez@gmail.com",
    description="API for remote note storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python:: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10.2",
    install_requires=[
        "fastapi[all]>=0.75.2",
        "passlib[bcrypt]>=1.7.4",
        "python-jose[cryptography]>=3.3.0",
        "python-multipart==0.0.5",
        "uvicorn>=0.17.6",
    ]
)
