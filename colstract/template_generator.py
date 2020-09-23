import pathlib

from colstract.config import Config
from colstract.xresource_reader import XReader
from colstract.logger import Logger


class TemplateGenerator(object):
    def __init__(self, path: str = None):
        self.config_options = Config(path)
        self.parser = XReader(path)
        self.logger = Logger(name='colstract-generator', log_file=self.config_options.log_file).get_logger()
        self.templates = self._templates()

    @staticmethod
    def _templates() -> list:
        path = pathlib.Path(__file__).parent / 'templates'
        result = [thing for thing in path.iterdir() if thing.is_file()]
        return result

    def generate(self):
        for item in self.templates:
            item: pathlib.Path
            self.logger.info(f"creating {item.name}")
            with open(item, 'r') as file:
                template_blank: str = file.read()

            result = template_blank.format(
                **self.parser.parsed_data,
                **self.parser.parsed_data['special'],
                **self.parser.parsed_data['colors']
            )

            output_dir = pathlib.Path(self.config_options.config.get('output_dir'))
            if not output_dir.exists():
                self.logger.warning(f"{output_dir} not present, attempting to create it")
                pathlib.Path.mkdir(output_dir, parents=True)
                self.logger.info(f"Created {output_dir}")

            output_file = output_dir / item.name
            with open(str(output_file), 'w') as out_:
                out_.write(result)
                self.logger.info(f"Generated {output_file}")
                print(f"Generated {output_file}")
