import json
from json import dumps
import sys
import os
from Mining import Mining
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

mining = Mining(os.getenv("TOKEN"))
print(json.dumps(mining.run_github_query(), sort_keys=True, indent=4))