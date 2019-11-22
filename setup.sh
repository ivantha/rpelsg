# upgrade pip
py -m pip install --upgrade pip

# install virtualenv
python3 -m pip install --user virtualenv

# create a virtual environment
python3 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install requirements
pip install -r requirements.txt

# deactivate the virtual environment
deactivate