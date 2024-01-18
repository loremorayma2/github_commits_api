GitHub Commits API REST
Overview

The GitHub Commits API REST project is a Django-based REST API that allows you to retrieve and store GitHub commits using Python. This API is designed to provide an easy way to access and manage commit data from GitHub repositories.
Requirements

Before using this project, make sure you have the following requirements:

    Python 3.x installed on your system.
    Django 3.x and the necessary dependencies installed. You can install them using the provided requirements.txt file.
    A GitHub account and a personal access token for authentication.

Usage

This API enables you to retrieve commits from specific GitHub users and store them in the database. You can interact with the API by sending HTTP POST requests to the appropriate endpoint. Be sure to follow the API documentation for details on how to use it effectively.
Configuration

To configure the project:

    Create a .env file in the project's root directory and define the following environment variables:

    makefile

GITHUB_URL=https://api.github.com/
GITHUB_ACCESS_TOKEN=YOUR_GITHUB_PERSONAL_ACCESS_TOKEN

Run migrations to create the necessary database tables:

    python manage.py makemigrations
    python manage.py migrate

Dependencies

The project's dependencies are listed in the requirements.txt file. You can install them using pip:

pip install -r requirements.txt

Notes

    This API uses caching to improve performance by storing data for 15 minutes before re-querying GitHub. You can customize the caching settings to suit your needs.

    Ensure that you configure security and permissions appropriately before deploying this API in a production environment.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Enjoy using the GitHub Commits API REST for your project!
