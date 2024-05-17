# ChatWithPythonFlask

This is the documentation to understant every part of the project.

Important things to know after starting this project: <br>
    - You need to have at least some knowledge about Python and Flask. <br>
    - MongoDB it's our medium to store the data, you need to have an Account. <br>
    - This chat explains how to create multiple programs, cli tools and more. <br>
    - The duration of this course is of about: 1 week. <br>
    - Want some help? Send us an email: support_learning@devcraftsofware.com

## Setting Up Everything

Let's start with this amazing **CHAT APP**, but first we need to set up some things for it to work
propperly, so scroll down and setup the project with me

1. **Create your Project Directory**:
This is our first step, you are going to navigate with the terminal, into the directory you want
and then you need to write the next command:
<br>

```bash
    $> mkdir your_awesome_python_chat_app
```
2. **Access the directory and create your venv**:
Now we need to setup our isolated enviroment with python to work in a more
tiddy project, venvs if you don't know what they are, heres a little explanation:
>**Virtual environments**, or **"venvs"**, in Python are a tool that allows you to create isolated spaces for your Python projects. Each venv can have its own version of Python and its own installed packages, which helps to avoid conflicts between dependencies of different projects.

```bash
    # First we check the version of python
    $> python --version
    #OUTPUT: Python 3.12.3 (It does not need to be this version but a newer Ver is recomended)

    # Now we execute the venv module with python to put up a venv
    $> python -m venv env # You can choose any name, but I preffer to have it located.

    # In case it fails:
    $> python -m pip install virtualenv
    # Repeat the steps above.
```

3. **Activatus Maximus...**:
Now the only step it's left for us to do (TO SETUP THE VENV), it's activating it! <br>
this step will start the virtual enviroment, so to do that you only need to do the
next:

```bash
    # If you are on Linux/Mac:
    $> source ./env/bin/activate

    # If you are on Windows
    $> ./env/Scripts/activate
```

This will prompt us the next thing on our **terminal**:

```bash
    (env) $path $> _ 
```

We are ready to start working in the project!

Let's go! Next Step: [Next Steps->](setup.md)