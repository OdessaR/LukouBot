#!/bin/bash
cd /home/pi/Desktop/LukouBot/
date >> log
echo starting bot >> log 2>&1
DISPLAY=:0 python3 main.py >> log 2>&1
DISPLAY=:0 python3 post_bot.py >> log 2>&1

