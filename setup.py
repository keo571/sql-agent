# setup.py
from setuptools import setup, find_packages

setup(
    name="sql-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.0.0",
        "sqlalchemy>=1.4.0",
        "transformers>=4.0.0",
        "python-dotenv>=0.19.0",
        "pytest>=6.0.0",
        "black>=21.0.0",
        "flake8>=3.9.0",
        "torch>=2.0.0",
        "openai>=1.0.0",
    ],
    author="SQL Agent Team",
    author_email="team@sqlagent.dev",
    description="An intelligent SQL agent for database interactions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/keo571/sql-agent.git",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)