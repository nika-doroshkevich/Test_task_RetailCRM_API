#!/bin/bash

uvicorn app.main:main_app --host 0.0.0.0 --port 8000 --reload