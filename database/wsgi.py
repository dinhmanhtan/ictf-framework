#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import app

if __name__ == "__main__":
    app.run(port=80,debug=True,host="0.0.0.0",use_debugger=False)

