from clld.web.assets import environment
from clldutils.path import Path

import parabank


environment.append_path(
    Path(parabank.__file__).parent.joinpath('static').as_posix(),
    url='/parabank:static/')
environment.load_path = list(reversed(environment.load_path))
