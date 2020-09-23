import subprocess
import pathlib

from colstract.config import Config
from colstract.logger import Logger


class Reload(object):
    def __init__(self, path: str = None):
        self.config_options = Config(path)
        self.logger = Logger(log_file=self.config_options.log_file, name='colstact-reload').get_logger()

    def xrdb(self) -> int:
        if not self.exists('xrdb'):
            self.logger.error("xrdb does not exist")
            return 1

        self.logger.info("Attempting to merge xrdb")
        command = [
            'xrdb',
            '-merge',
            str(pathlib.Path(self.config_options.config.get('output_dir')) / 'colors.Xresources')
        ]

        self.logger.info(f"Running {' '.join(command)}")

        output_raw = subprocess.run(command, capture_output=True)
        return_code = output_raw.returncode
        output = output_raw.stdout.decode('utf-8').strip('\n')

        self.logger.info(f"The process completed with he stdout {output}")
        self.logger.info(f"The return code is : {return_code}")

        return return_code

    def tty(self) -> int:
        self.logger.info(f"Attempting to apply color scheme to TTY")
        command = [
            "sh",
            str(pathlib.Path(self.config_options.config.get("output_dir")) / 'colors-tty.sh')
        ]
        self.logger.info(f"Running command {' '.join(command)}")
        output_raw = subprocess.run(command, capture_output=True)
        output = output_raw.stdout.decode('utf-8').strip('\n')
        return_code = output_raw.returncode

        self.logger.info(f"The process exited with the stdout: {output}")
        self.logger.info(f"The return code is: {return_code}")

        return return_code

    def i3(self) -> int:
        if not self.exists('i3-msg'):
            self.logger.error("i3-msg does not exist")
            return 1

        self.logger.info("Attempting to reload i3-wm")
        command = [
            "i3-msg",
            "reload"
        ]

        self.logger.info(f"Running command {' '.join(command)}")
        output_raw = subprocess.run(command, capture_output=True)
        output = output_raw.stdout.decode('utf-8').strip('\n')
        return_code = output_raw.returncode

        self.logger.info(f"The process exited with the stdout: {output}")
        self.logger.info(f"The return code is: {return_code}")

        return return_code

    def bspwm(self) -> int:
        if not self.exists('bspc'):
            self.logger.error("bspc does not exist")
            return 1

        self.logger.info("Attempting to reload bspwm")
        command = [
            "bspc",
            "wm",
            "-r"
        ]

        self.logger.info(f"Running command {' '.join(command)}")
        output_raw = subprocess.run(command, capture_output=True)
        output = output_raw.stdout.decode('utf-8').strip('\n')
        return_code = output_raw.returncode

        self.logger.info(f"The process exited with the stdout: {output}")
        self.logger.info(f"The return code is: {return_code}")

        return return_code

    def kitty(self) -> int:
        if not self.exists('kitty'):
            self.logger.error("kitty does not exist")
            return 1

        self.logger.info("Attempting to reload kitty")
        command = [
            "kitty",
            "@",
            "set-colors",
            "--all",
            str(pathlib.Path(self.config_options.config.get("output_dir")) / 'colors-kitty.conf')
        ]

        self.logger.info(f"Running command {' '.join(command)}")
        output_raw = subprocess.run(command, capture_output=True)
        output = output_raw.stdout.decode('utf-8').strip('\n')
        return_code = output_raw.returncode

        self.logger.info(f"The process exited with the stdout: {output}")
        self.logger.info(f"The return code is: {return_code}")

        return return_code

    def polybar(self) -> int:
        self.logger.info("Attempting to reload polybar")
        command = [
            "pkill",
            "-USR1",
            "polybar"
        ]

        self.logger.info(f"Running command {' '.join(command)}")
        output_raw = subprocess.run(command, capture_output=True)
        output = output_raw.stdout.decode('utf-8').strip('\n')
        return_code = output_raw.returncode

        self.logger.info(f"The process exited with the stdout: {output}")
        self.logger.info(f"The return code is: {return_code}")

        return return_code

    def sway(self) -> int:
        if not self.exists('swaymsg'):
            self.logger.error("swaymsg does not exist")
            return 1

        self.logger.info("Attempting to reload sway")
        command = [
            "swaymsg",
            "reload"
        ]

        self.logger.info(f"Running command {' '.join(command)}")
        output_raw = subprocess.run(command, capture_output=True)
        output = output_raw.stdout.decode('utf-8').strip('\n')
        return_code = output_raw.returncode

        self.logger.info(f"The process exited with the stdout: {output}")
        self.logger.info(f"The return code is: {return_code}")

        return return_code

    def reload_all(self) -> None:
        self.logger.info("Attempting to reload environment")
        if self.xrdb() != 0:
            self.logger.error("Reloading xrdb failed")
        if self.tty() != 0:
            self.logger.error("Reloading TTY failed")
        if self.i3() != 0:
            self.logger.error("Reloading i3-wm failed")
        if self.bspwm() != 0:
            self.logger.error("Reloading bspwm failed")
        if self.sway() != 0:
            self.logger.error("Reloading sway failed")
        if self.kitty() != 0:
            self.logger.error("Reloading Kitty failed")
        if self.polybar() != 0:
            self.logger.error("Reloading  polybar failed")
        return

    @staticmethod
    def exists(program):
        output = subprocess.run(['which', program], capture_output=True)
        if "not found" in output.stdout.decode('utf-8').strip('\n'):
            return False
        elif output.returncode == 1:
            return False
        else:
            return True
