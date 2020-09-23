import pathlib
import json
import subprocess

from colstract.logger import Logger
from colstract.config import Config


class WallSetter(object):
    def __init__(self, path: str = None):
        self.config_options = Config(path)
        self.walconfig = pathlib.Path(__file__).parent / 'walconfig'
        self.log_file = self.config_options.log_file
        self.logger = Logger(name='colstract-wallpaper_setter', log_file=self.log_file).get_logger()

    def wallpaper_apply(self, backend: str) -> int:
        """
        Apply wallpaper using provided backend
        Currently only these backends are supported: (feh, nitrogen)
        :param backend:
        :return:
        """
        if backend not in ('feh', 'nitrogen'):
            self.logger.error(f"{backend} is not supported as of this version")
            print(f"{backend} is not supported as of this version")
            return 1
        self.logger.info(f"Using {backend} as backend for setting wallpaper")
        default_option = '--bg-fill' if backend == 'feh' else '--set-scaled'
        with open(self.walconfig / f'{backend}.json', 'r') as file:
            options: dict = json.loads(file.read())
            self.logger.info(f" {backend} configuration file {backend}.json loaded")

        set_options = self.config_options.config.get('wallpaper_options').get('setter_option')
        if set_options is None:
            self.logger.warning(f"No setter options provided, using {default_option}")
            set_options = default_option
        elif set_options in options.get('options'):
            self.logger.info(f"Using {set_options} option to set wallpaper")
            pass
        else:
            self.logger.warning(f"Invalid parameter {set_options}. Using default option: {default_option}")
            set_options = default_option

        function_call = subprocess.run(['which', backend], capture_output=True)
        if function_call.returncode == 0:
            program_path = function_call.stdout.decode('utf-8').strip('\n')
            self.logger.info(f"{backend} located at {program_path}")
        else:
            self.logger.error(f"failed to locate program {backend}")
            print(f"failed to locate {backend}")
            return 1

        self.logger.info(
            f"Calling: {program_path} {set_options} {self.config_options.config.get('wallpaper_options').get('path')}"
        )

        output = subprocess.run(
            [
                program_path,
                set_options,
                self.config_options.config.get('wallpaper_options').get('path')
            ]
        ).returncode
        if output == 0:
            self.logger.info("Wallpaper applied successfully")
            print("Wallpaper applied successfully")
        else:
            self.logger.error(f"Failed to apply wallpaper. Return Code: {output}")
            print(f"Failed to apply wallpaper with return code {output}")

        return 0
