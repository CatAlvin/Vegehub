import os
import logging.config
import yaml

__current_folder = os.path.dirname(os.path.abspath(__file__))

def setup_logging(default_path= os.path.join(__current_folder, 'config', 'logging-config.yaml'), default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt', encoding='utf-8') as f:
            config = yaml.safe_load(f.read())
        # 确保日志文件的目录存在
        log_file_path = config['handlers']['file']['filename']
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        logging.config.dictConfig(config)
        
    else:
        print('!!!!!!!!!logging config file not found, using basicConfig!!!!!!!!!!!!')
        logging.basicConfig(level=default_level)

setup_logging()