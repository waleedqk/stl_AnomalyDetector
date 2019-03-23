# Python Virtual Environment

## ssh into the system

    ssh -i ~/.ssh/esg_compute wqkhan@compute1.esg.uwaterloo.ca
    ssh -i ~/.ssh/esg_compute wqkhan@compute2.esg.uwaterloo.ca    

## System Configuration

### Python Path

Make sure the PYTHONPATH env variable is up to data

    export PYTHONPATH=${PYTHONPATH}:/rhome/wqkhan/.local/lib/python3.5/site-packages

### Update the Python Installation

In case of some errors ```from pip import main``` happens when you inadvertently upgraded your system pip. To fix this: 

    python3 -m pip uninstall pip
    python3 -m pip install --user pip

The particular issue seems to be:

1) pip3 install --user --upgrade pip installs pip in the user site, but doesn't uninstall the system site copy of pip.
2) User runs the system wrapper from /usr/bin/pip3 which is from the OS-supplied pip. 

Whatever the first valid location is in the $PATH is what takes priority in the installation.

    vim /rhome/wqkhan/.bashrc
    
Add ```PATH=/rhome/wqkhan/.local/bin:$PATH``` for the user site to take priority 
Or ```PATH=$PATH:/rhome/wqkhan/.local/bin``` for the system wrapper to take priority


    source /rhome/wqkhan/.bashrc
    echo $PATH

### Installing the proper Packages

    python3 -m pip install --user --upgrade pip
    pip3 install virtualenv --user
    pip3 install virtualenv --user --upgrade
    pip3 show virtualenv
    virtualenv --version
    
### View Python installtion locations

    python3 -m site
    python3 -m site --user-site

## Create a Virtual Environment

### Create Folder Space

    mkdir -p ~/py_venv
    cd /rhome/wqkhan/py_venv/
    
### Specify Name and Python Version of Env

    python -m virtualenv -p python3 /rhome/wqkhan/py_venv/dataAnalytics
    
### Activate the Virtual Environment

    source /rhome/wqkhan/py_venv/dataAnalytics/bin/activate

    
### Install Packages in Virtual Environment

Create a requirements document ```requirements.txt``` that contains a list of the needed pacakages:

Install the specified packages using the following command:

    pip3 install -r /rhome/wqkhan/py_venv/requirements.txt
    
### Freezing dependencies

Pip can export a list of all installed packages and their versions using the freeze command:

    pip freeze
        
### Deactivate the Virtual Environment

    deactivate