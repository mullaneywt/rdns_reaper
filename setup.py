import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()


version = "0.0.12"

platforms = "OS Independent"

classifiers = [
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "Intended Audience :: System Administrators",
    "Intended Audience :: Telecommunications Industry",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Topic :: Internet",
    "Topic :: Internet :: Name Service (DNS)",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Quality Assurance",
    "Topic :: Software Development :: Testing",
    "Topic :: System :: Networking",
    "Topic :: Utilities",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

setuptools.setup(
    name="rdns_reaper",
    version=version,
    author="Will Mullaney",
    author_email="rdns-reaper@mullaneywt.anonaddy.com",
    classifiers=classifiers,
    description="Reverse DNS lookup engine",
    install_requires=["netaddr>=0.8.0", "pyyaml>=6.0"],
    keywords=["reverse dns", "dns"],
    license="GNU GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["rdns_reaper"],
    platforms=platforms,
    python_requires=">=3.6",
    project_urls={"Bug Tracker": "https://github.com/mullaneywt/rdns_reaper/issues"},
    url="https://github.com/mullaneywt/rdns_reaper",
)
