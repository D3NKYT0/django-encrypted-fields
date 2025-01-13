from setuptools import setup, find_packages

setup(
    name="django-encrypted-fields",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["Django>=4.2", "cryptography>=44.0.0", "pillow>=11.1.0"],
    author="Denky",
    author_email="contato@denky.dev.br",
    description="Campos e storages criptografados para o Django.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/D3NKYT0/django-encrypted-fields",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.10",
)
