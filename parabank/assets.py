import pathlib

from clld.web.assets import environment

import parabank


environment.append_path(
    str(pathlib.Path(parabank.__file__).parent.joinpath('static')), url='/parabank:static/')
environment.load_path = list(reversed(environment.load_path))
