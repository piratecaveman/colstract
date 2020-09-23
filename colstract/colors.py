class Color(object):
    def __init__(self, hexadecimal: str):
        self.hexadecimal = hexadecimal.lower()
        if not self.valid:
            raise ValueError("A hexadecimal color is formatted like #000000")
        self.alpha_value = 100

    @property
    def valid(self) -> bool:
        if not self.hexadecimal.startswith('#'):
            return False
        else:
            if len(self.hexadecimal) > 9:
                return False
            elif len(self.hexadecimal) < 7:
                return False
            else:
                if all(x in 'abcdef0123456789' for x in self.strip):
                    return True
                else:
                    return False

    def __str__(self) -> str:
        return self.hexadecimal

    @property
    def strip(self) -> str:
        return self.hexadecimal[1:]

    @property
    def rgb(self) -> str:
        if len(self.strip) == 6:
            r, g, b = (int(self.strip[0:2], 16), int(self.strip[2:4], 16), int(self.strip[4:6], 16))
            return f'{r},{g},{b}'

    @property
    def rgba(self) -> str:
        r, g, b = (int(self.strip[0:2], 16), int(self.strip[2:4], 16), int(self.strip[4:6], 16))
        if len(self.strip) == 8:
            a = int(self.strip[6:8]) / 100
        else:
            a = self.alpha_value / 100
        return f'rgba({r},{g},{b},{a})'

    @property
    def alpha(self) -> str:
        if len(self.strip) == 8:
            alpha_ = f'[{self.hexadecimal[7:9]}]{self.hexadecimal[0:7]}'
        else:
            alpha_ = f'[{self.alpha_value}]{self.hexadecimal}'
        return alpha_

    @property
    def xrgba(self) -> str:
        return '{0}{1}/{2}{3}/{4}{5}/ff'.format(*self.strip,)
