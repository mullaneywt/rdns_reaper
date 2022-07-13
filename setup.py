import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='rdns_reaper',
    version='0.0.6',
    author='Will Mullaney',
    author_email='rdns-reaper@mullaneywt.anonaddy.com',
    description='Reverse DNS lookup engine',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mullaneywt/rdns_reaper',
    project_urls = {
        "Bug Tracker": "https://github.com/mullaneywt/rdns_reaper/issues"
    },
    license='None',
    packages=['rdns_reaper'],
    install_requires=['netaddr', 'pyyaml'],
)
