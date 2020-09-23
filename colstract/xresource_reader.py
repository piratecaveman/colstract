import re

from colstract.colors import Color
from colstract.config import Config
from colstract.logger import Logger


class XReader(object):
    def __init__(self, path: str = None):
        self.config_options = Config(path)
        self.log_file = self.config_options.log_file
        self.logger = Logger(name='colstract-xreader', log_file=str(self.log_file)).get_logger()
        self.content = self._read()
        self.compiled_patterns = self._compiled_patterns()
        self.parsed_data = self._parsed()

    def _read(self):
        with open(self.config_options.config.get('xresources_path'), 'r') as file:
            data = file.read()
            self.logger.info(f"Read Xreources file at {self.config_options.config.get('xresources_path')}")
        return data

    @staticmethod
    def _compiled_patterns() -> dict:
        color = r'#[A-Fa-f0-9]{6,8}'
        color_number = r'color[0-9]{1,2}'
        patterns = {
            'background': re.compile(f'background:.*({color})'),
            'foreground': re.compile(f'foreground:.*({color})'),
            'cursor': re.compile(f'cursorColor:.*({color})'),
            'colors': re.compile(f'({color_number}).*({color})')
        }
        return patterns

    def _parsed(self) -> dict:
        output = {
            'wallpaper': self.config_options.config.get('wallpaper_options').get('path'),
            'alpha': '100',
            'special': {
                'background': Color(re.findall(self.compiled_patterns['background'], self.content)[0]),
                'foreground': Color(re.findall(self.compiled_patterns['foreground'], self.content)[0]),
                'cursor': Color(re.findall(self.compiled_patterns['cursor'], self.content)[0])
            },
            'colors': {}
        }
        colors = re.findall(self.compiled_patterns['colors'], self.content)
        colors.sort(key=lambda x: int(x[0][5:]))
        for item in colors:
            output['colors'][item[0]] = Color(item[1])
        return output
