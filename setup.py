import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="rdns_reaper",
    version="0.0.12.post1",
    author="Will Mullaney",
    author_email="rdns-reaper@mullaneywt.anonaddy.com",
    description="Reverse DNS lookup engine",
    install_requires=["netaddr>=0.8.0", "pyyaml>=6.0"],
    keywords=["reverse", "dns"],
    license="None",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["rdns_reaper"],
    python_requires=">=3.6",
    project_urls={
        "Bug Tracker": "https://github.com/mullaneywt/rdns_reaper/issues",
        "Source": "https://github.com/mullaneywt/rdns_reaper/",
        "Documentation": "https://rdns-reaper.readthedocs.io/",
    },
    url="https://github.com/mullaneywt/rdns_reaper",
)
