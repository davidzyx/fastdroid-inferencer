from src.decompile import apktool_decompile
from src.smali import SmaliApp
from src.hindroid import HindroidInferencer

import pandas as pd
import os
import sys
from hashlib import blake2s

def run(arg):
    # Decompile
    if os.path.isfile(arg) and arg.endswith('apk'):
        app_dir = blake2s(os.path.basename(arg).encode(), digest_size=16).hexdigest()
        app_dir = os.path.join(os.path.dirname(arg), app_dir)
        if not os.path.exists(app_dir):
            apktool_decompile(arg, app_dir)
    else:
        assert os.path.isdir(arg)
        app_dir = arg

    # Read relevant APIs
    apis = pd.read_csv('model/APIs.csv', names=['API']).API
    pattern = f"({'|'.join(apis.tolist())})"

    # Parse
    print(arg)
    app = SmaliApp(app_dir, pattern)
    model = HindroidInferencer(app.info, 'model/')

    print(model.predict_AA())
    print(model.predict_APA())
    print(model.predict_ABPBA())


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        run(arg)
