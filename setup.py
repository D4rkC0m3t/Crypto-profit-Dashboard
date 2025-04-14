from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("src/requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="tradeprofitanalytics",
    version="0.1.0",
    author="TradeProfitAnalytics Team",
    author_email="info@tradeprofitanalytics.com",
    description="A comprehensive dashboard for analyzing cryptocurrency exchange performance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/TradeProfitAnalytics",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tradeprofitanalytics=main:main",
        ],
    },
)
