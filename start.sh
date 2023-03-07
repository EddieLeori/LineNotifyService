#!/bin/bash
mkdir -p log
nohup python app.py >> log.txt 2>&1 &

