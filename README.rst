===============
TPO-Backend-App
===============

This is a short guide on overall project Structure and setting up the system and environment dependencies
required for the application to run.

Project Structure
-----------------

``app/db.py`` contains all database interfacing method or DAO

The API layer is implemented in the ``app/api`` directory and it contains all the `Flask Blueprint <https://flask.palletsprojects.com/en/1.1.x/blueprints/>`_

The ``run.py`` file is the application's entry point, the `config.py` file contains the application configurations, and the ``requirements.txt`` file contains the software dependencies for the application.

Function ``create_app`` in the ``app/__init__.py``, given a configuration name, loads the correct configuration from the ``config.py`` file, as well as the configurations from the ``instance/config.py`` file.

Local Development Environment Configuration
-------------------------------------------
1. Download the latest version of Python from `Python official website <https://www.python.org/downloads/>`_
2. Fork the project, clone your fork, and configure the remotes::

    # Clone your fork of the repo into the current directory
    git clone https://github.com/<your-username>/TPO-Backend-App.git
    # Navigate to the newly cloned directory
    cd TPO-Backend-App
    # Assign the original repo to a remote called "upstream"
    git remote add upstream https://github.com/aissmstpo/TPO-Backend-App.git

3. If you cloned a while ago, get the latest changes from upstream::
 
    git checkout master
    git pull upstream master

4. Create the virtual environment for application::
  
    # navigate to the TPO-Backend-App
    cd TPO-Backend-App

    # create the virtual environment
    python -m venv tpo_venv

    # activate the virtual environment
    source tpo_venv/bin/activate

    # install the dependencies
    pip install -r requirements.txt
    
4. Create a new topic branch (off the main project development branch) to contain your feature, change, or fix::

    git checkout -b <topic-branch-name>

5. Commit your changes
6. Push your topic branch up to your fork::
    
    git push origin <topic-branch-name>

7. Open a Pull Request with a clear title and description.
8. After your Pull Request is away, you might want to get yourself back onto master and delete the topic branch::

    git checkout master
    git branch -D <topic-branch-name>
