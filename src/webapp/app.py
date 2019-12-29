import sys
from inspect import getframeinfo, currentframe
from pathlib import Path

filename = getframeinfo(currentframe()).filename
current_module_path = Path(filename).resolve().parent

ROOT_PATH = Path(current_module_path).parents[0].as_posix()
print(ROOT_PATH)
module_path_list = [
    f"{ROOT_PATH}/",
    f"{ROOT_PATH}/utils",
]

for index, path in enumerate(module_path_list):
    sys.path.insert(index, path)

from webapp import app, db


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=9898)
