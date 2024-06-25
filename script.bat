@echo off

REM This script is used to build all necessary python components and run Django website.

REM Install necessary Python components
pip install .\football_data_source
pip install .\hotel_data_soruce
pip install .\simple_visualizer
pip install .\block_visualizer

REM Run Django website
@REM cd %1
cd graph_visualization
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
