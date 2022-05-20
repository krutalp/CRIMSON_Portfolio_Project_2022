import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="friedBrains",
    version="1.0.0",
    author="Krutal Patel",
    author_email="kpate111@jhu.edu",
    description="CRIMSON 2022 Portfolio Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "scipy", "rich", "click"],
    include_package_data=True,
    python_requires=">=3.9",
)
