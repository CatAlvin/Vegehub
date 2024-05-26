# Construct python environment
1. Make sure use python 3.10 or use conda to create a new environment
```bash
conda create -n py310 python=3.10.12
conda activate py310
```
2. Create a virtual environment
```bash
python -m venv ./venv
```
3. Install the required packages
```bash
pip install -r requirements.txt
```

# How to initialize the database
1. Configure the `database-config.txt` in `./database/config/` to connect to the database
2. Can use the sqlachemy models in `./database/models.py` to operate the database
3. Simple initialization of the database
```bash
python initDatabase.py
```
1. Use `database.utils` to get the useful functions
2. Use `database.models` to get the orm models
3. Use `database.api` to get the database api

# How to use the logger api
1. Import the logger setup file
```python
import logging
from logger import logging_setup
```
2. Create a logger object in your .py file
```python
logger = logging.getLogger(__name__)
```
3. Use the logger object to log the messages
```python
logger.debug("This is a debug message") # in logs.txt
logger.info("This is an info message") # in console and logs.txt
logger.error("This is an error message") # in console and logs.txt
```
4. find the logs in `./logger/logData/logs.txt`

# How to run the backend
1. Run the backend server
```bash
python runBackend.py
```
2. The backend server will run on `http://localhost:8000/`
3. The backend server will run on `http://localhost:8000/docs` to see the api documentation

# How to run the frontend
1. Download vscode `live server` extension
2. Use `live server` to run the frontend on `http://localhost:5500/` or `http://localhost:5501/`

# How to run the GUI
1. Run the GUI
```bash
python runVegehub.py
```

# How to create the visualizations
1. The functions under `dataVisualization` module can be used to create the visualizations
```python
# For example, to draw the customer gender age butterfly chart
from dataVisualization import *
draw_customer_gender_age_butterfly_chart()
```

# Git commands
1. To clone the repository (now it is public)
```bash
git clone https://github.com/CatAlvin/Vegehub.git
```