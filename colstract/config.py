import os
import pathlib
import json
import copy


from colstract.logger import Logger


class Config(object):
    def __init__(self, path: str = None):
        self.default_path = pathlib.Path(os.environ['HOME']) / '.config' / 'colstract' / 'config.json'
        self.default_output = pathlib.Path(os.environ['HOME']) / '.cache' / 'colstract'
        self.default_xresources = pathlib.Path(os.environ['HOME']) / '.Xresources'
        self.log_file = pathlib.Path(os.environ['HOME']) / '.cache' / 'colstract' / 'log' / 'colstract.log'
        self.template = {
            'output_dir': None,
            'xresources_path': None,
            'wallpaper_options': {
                "apply_wallpaper": False,
                "path": None,
                "setter": None,
                "setter_option": None
            }
        }
        # logger
        self.logger = Logger(name='colstract-config', log_file=str(self.log_file)).get_logger()

        # config path if provided
        self.__path: str = path
        self.path = self._path()
        self.config = self._config()

    def _path(self) -> pathlib.Path:
        path_ = None
        if self.__path is None:
            self.logger.info(f'Using default path: {self.default_path} - no custom path provided')
            path_ = self.default_path
        elif self.__path is not None:
            path_ = pathlib.Path(self.__path)
            if not path_.exists():
                self.logger.warning(f'{path_} does not exist. Using default path: {self.default_path}')
                path_ = self.default_path
            else:
                self.logger.info(f'Using custom config path {path_}')
        return path_

    def _config(self) -> dict:
        if not self.path.exists():
            self.logger.error(f'{self.path} does not exist')
            raise FileNotFoundError(f"{self.path} does not exist")

        with open(self.path, 'r') as file:
            data: dict = json.loads(file.read())
            self.logger.info(f'config read from {self.path}')

        config_ = copy.deepcopy(self.template)

        config_['output_dir'] = data.get('output_dir')
        if config_['output_dir'] is None:
            self.logger.info(f'output directory not specified. Using default {self.default_output}')
            config_['output_dir'] = self.default_output

        config_['xresources_path'] = data.get('xresources_path')
        if config_['xresources_path'] is None:
            self.logger.info(f'xresources file not specified. Using default {self.default_xresources}')
            config_['xresources_path'] = self.default_xresources

        # wallpaper options logging
        config_['wallpaper_options'].update(data.get('wallpaper_options', self.template.get('wallpaper_options')))

        # if it is to be applied
        if config_['wallpaper_options']['apply_wallpaper']:
            self.logger.info('apply_Wallpaper is True. Wallpaper will be applied if path is provided')

            # if path actually exists
            if pathlib.Path(str(config_['wallpaper_options']['path'])).exists():
                self.logger.info(f'Wallpaper file exists')

            else:
                self.logger.error(f'Wallpaper file does not exist at {config_.get("wallpaper_options").get("path")}')
        else:
            self.logger.info('apply_wallpaper is False. Wallpaper will not be processed')

        return config_
