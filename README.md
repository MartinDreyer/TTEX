# TTEX

# Project Setup Guide

Follow these steps to set up the project environment and get everything running.

## Prerequisites

Ensure you have Python and Node.js on your system

## Repository Cloning

First, clone the repository to your local machine:

```bash
git clone https://github.com/MartinDreyer/TTEX.git
cd TTEX
```

## Environment Setup

Set up the environment variables needed for the project:

```plaintext
touch .env
```

Edit the `.env` file and fill in the necessary details.

## Python Virtual Environment

Create and activate a Python virtual environment, and install the required Python packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Node.js Dependencies

Install the required Node.js packages:

```bash
npm install
```

## Tailwind CSS Build

Build the Tailwind CSS files:

```bash
python3 manage.py tailwind build
```

## Static Files Collection

Collect static files for Django:

```bash
python3 manage.py collectstatic
```

## Database Migrations and Superuser Creation

Migrate to make sure your database is up to date, and then create a new superuser

```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```

Follow the prompts to create a superuser.

## Final Steps

After setting up everything, you can sign in with the superuser account via [http://localhost:8000/admin](http://localhost:8000/admin) and change the hostname or other settings as necessary.
