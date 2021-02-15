import json
import sys
import os
from dotenv import load_dotenv, find_dotenv
from Mining import Mining


load_dotenv(find_dotenv())
SECRET_KEY = os.getenv("TOKEN")

mining = Mining("5fa50a6904490d2b3d04f254e4f36339b1e02226")
print(json.dumps(mining.run_github_query(), sort_keys=True, indent=4))