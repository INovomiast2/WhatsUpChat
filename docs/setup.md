# Project Setup

This guide will walk you through the steps to set up a Python Flask project.

## Prerequisites

Before you begin, make sure you have the following installed on your machine:

- **Python** (version 3.6 or higher)
- **pip** (Python package installer)

## Step 1: Install all Python Packages

1. Install Flask and Flask_SockeIO:

```bash
    $> python -m pip install flask flask_socketio
```

2. Install simple_term_menu and survey, add colorama and other packages:

This modules will be used when we develop all the cli tools to manipulate
and control the webapp.

```bash
    $> python -m pip install survey colorama simple_term_menu
```
3. Install **pymongo**

PyMongo is used to control all the aspects of our **MongoDB** database.

```bash
    $> python -m pip install pymongo
```

4. Install **resend**