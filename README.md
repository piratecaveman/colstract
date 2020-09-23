# Colstract

Colstract is a color scheme template generator which parses Xresources files for colors and generates
templates for configuration of various programs using those colors. It is inspired from PyWal and offers
to create templates from the colors you provide. It does not generate color schemes. It can optionally set
a wallpaper for you using either feh or nitrogen.

## Requirements
```
setuptools (make)
wheel (make)
feh (optional)
nitrogen (optional)
```  
  
`setuptools` and `wheel` are require to build a package.  
To install them using pip:  
`pip install --user -r requirements.txt`  

## Build
To create a package, run in a terminal:  
`python setup.py bdist_wheel`  

## Install
After building the package to install it:  
`1. cd dist/`  
`2. pip install --user *.whl`

## Configuration
The program expects a config file to run. The 
default path the program looks for is `$HOME/.config/colstract/config.json`  
Using `-c` or `--config` a path can be provided to the config.json which if provided will be used.  
An example configuration file is provided in `colstract/examples/example_config.json`

## Usage
To use the program simply run: `python -m colstract`  
Or if you want to provide a config file: `python -m colstract --config /path/to/config.json`


## Output
The output path is `$HOME/.cache/colstract/`. This is, as of now, not change-able. 

## Reload Environment
If the option is set in the config, the program will optionally reload the following:
```
xrdb (merge)
TTY
i3-wm
bspwm
sway
kitty
polybar
```
And many others if you point their configurations to colstract's generated files.
For more info on how to setup various programs see PyWal's wiki:  [PyWal Wiki](https://github.com/dylanaraps/pywal/wiki/Customization)

## Wallpaper
The program can optionally apply a wallpaper for you if a wallpaper path is provided in the config.
Currently, only `feh` and `nitrogen` backends are supported. The backend you choose must be installed. 

## Logs
A simple log file is available at `$HOME/.cache/colstract/log/colstract.log` which is reset on every run
of the program.
