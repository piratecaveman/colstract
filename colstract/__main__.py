import argparse

from colstract.template_generator import TemplateGenerator
from colstract.config import Config
from colstract.wallpaper_setter import WallSetter
from colstract.reload import Reload


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '-c',
    '--config',
    action='store',
    dest='config_file',
    default=None,
    help="Usage: -c/--config /path/to/file"
)
args = arg_parser.parse_args()

config = Config(args.config_file)
if config.config.get('wallpaper_options').get('apply_wallpaper'):
    WallSetter(args.config_file).wallpaper_apply(config.config.get('wallpaper_options').get('setter'))

generator = TemplateGenerator(args.config_file)
generator.generate()

if config.config.get('reload_env') is True:
    reloader = Reload(args.config_file)
    reloader.reload_all()
exit(0)
