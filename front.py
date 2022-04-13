# -*- coding: utf-8 -*-

import requests
import pandas as pd

api_endpoint = "http://127.0.0.1:5000/list"
r = requests.get(api_endpoint)

df = pd.read_json(r.content)

print(df.head(5))