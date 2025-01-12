from setuptools import setup, find_packages

setup(
    name="django-encrypted-fields",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["Django>=3.2", "cryptography>=3.4"],
    author="Seu Nome",
    author_email="seu_email@example.com",
    description="Campos e storages criptografados para o Django.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seuusuario/django-encrypted-fields",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
