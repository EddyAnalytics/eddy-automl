# -*- coding: utf-8 -*-
import os

# load config from env variables
BOOTSTRAP_SERVERS = os.environ.get("BOOTSTRAP_SERVER", "kafka:9092")