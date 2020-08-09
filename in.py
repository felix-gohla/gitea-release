#!/usr/bin/env python
import sys
import json

if __name__ == '__main__':
    json.dump({"version": { "status": "static" }}, sys.stdout)

