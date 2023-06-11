import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

base_path = os.path.abspath(os.path.dirname(__file__))

requirements = []
with open(os.path.join(os.path.dirname(base_path), "requirements.txt")) as f:
    requirements = f.read().splitlines()

readme = ""
with open(os.path.join(os.path.dirname(base_path), "README.md")) as f:
    readme = f.read()


class PyTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["../tests"]  # Specify the tests folder
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name="UnlimitedGPT",
    author="Sxvxge",
    url="https://github.com/Sxvxgee/UnlimitedGPT",
    project_urls={
        "Documentation": "https://github.com/Sxvxgee/UnlimitedGPT/blob/main/README.md",
        "Issue tracker": "https://github.com/Sxvxgee/UnlimitedGPT/issues",
        "Changelog": "https://github.com/Sxvxgee/UnlimitedGPT/blob/main/CHANGELOG.md",
    },
    version="0.1.5.6",
    packages=["UnlimitedGPT", "UnlimitedGPT/internal"],
    py_modules=["UnlimitedGPT"],
    license="GPL-3.0 license",
    description="An unofficial Python wrapper for OpenAI's ChatGPT API",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    tests_require=["python-dotenv", "pytest"],
    cmdclass={"test": PyTestCommand},
    python_requires=">=3.8.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
