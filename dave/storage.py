import logging
from pathlib import Path
from typing import Tuple


class Storage:
    
    @staticmethod
    def root(base: str, identifier: str) -> Path:
        _root = Path('~', 'Info', base, identifier).expanduser()
        _root.mkdir(mode=0o700, parents=True, exist_ok=True)
        return _root
    
    @staticmethod    
    def container(base: Path, identifier: str) -> Path:
        _path = Path(base, identifier)
        _path.mkdir(mode=0o700, parents=True, exist_ok=True)
        return _path

    @staticmethod
    def path_must_exist(identifier: str) -> Path:
        _path = Path(identifier)
        _path.mkdir(mode=0o700, parents=True, exist_ok=True)
        return _path

    @staticmethod
    def dotenv(root: Path, ) -> Path:
        dotenv_identifier = Path(info, '.env')
        with open(dotenv_identifier, 'w') as target:
            # Default key - value pairs
            key = "SECRET_KEY"
            value = uuid.uuid4().hex
            target.write(f'{key:s}="{value:s}"\n')

            key = "DATABASE_URI"
            value = ""
            target.write(f'{key:s}="{value:s}"\n')

            key = "UPLOADS_FOLDER"
            value = ""
            target.write(f'{key:s}="{value:s}"\n')

            key = "LOGGING_LEVEL"
            value = get_constant(key, ["CRITICAL", "ERROR", "WARNING", "INFO"], "DEBUG")
            target.write(f'{key:s}="{value:s}"\n')    


    @staticmethod
    def initialize(base: str, identifier: str) -> Tuple[Path, Path, Path]:
        logging.info(f'{identifier} parameters')
        root = Storage.root(base, identifier)
        store_path = Storage.container(root, 'store')
        logs_path = Storage.container(root, 'logs')
        return root, store_path, logs_path

    @staticmethod
    def create(base: str, identifier: str) -> Tuple[Path, Path, Path]:
        logging.info(f'{identifier} parameters')
        root, store_path, logs_path = Storage.initialize(base, identifier)
        Storage.dotenv(root)
        logging.info(f" base_path: {base:s}")
        logging.info(f" root_path: {str(root):s}")
        logging.info(f"store_path: {str(store_path):s}")
        logging.info(f" logs_path: {str(logs_path):s}")
        return root, store_path, logs_path

    @staticmethod
    def read(base: str) -> Tuple[Path, Path, Path]:
        root, store_path, logs_path = Storage.initialize(base, identifier)
        return root, store_path, logs_path
