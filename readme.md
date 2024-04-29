# How to use database
1. create a virtual environment
```bash
python -m venv ./venv
```
2. Install the required packages
```bash
pip install -r requirements.txt
```
3. Configure the `database-config.txt` in `./database/config/` to connect to the database
4. Can use the sqlachemy models in `./database/models.py` to operate the database
5. Simple initialization of the database
```bash
python sample.py
```
6. Use `utils.py` to get the useful functions for the project

# How to use the logger
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