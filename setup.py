#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="modeemintternet",
    description="Modeemi ry website",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    keywords="atk klubi uutiset club mate",
    author=", ".join(["Modeemi ry"]),
    author_email="hallitus@modeemi.fi",
    maintainer="Modeemi ry",
    maintainer_email="hallitus@modeemi.fi",
    url="https://github.com/modeemi/website",
    project_urls={
        "Documentation": "https://github.com/modeemi/website/wiki",
        "Source": "https://github.com/modeemi/website",
        "Tracker": "https://github.com/modeemi/website/issues",
    },
    license="BSD",
    package_dir={"modeemintternet": "modeemintternet"},
    python_requires="~=3.12",
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications",
    ],
    zip_safe=False,
)
