# **Irrigator Dashboard**

Control interface for remote watering system, still in  development.
This is the final project for Multimedia Design and Production course at the Faculty of Engineering of the University of Florence

Application features:
----- 
- Weather forecast

- Control multiples gardens per account and create different watering areas

- For each area you can choose between 3 irrigation types:
  - **manual**
  
    irrigation starts by activating a timer for selected time
  - **scheduled**
  
    decide frequency, time duration and start hour of irrigation
  - **smart**
  
    computer decides when it's the best time to start watering the area and how long it has to last. All this decisions are based on humidity and  last rain  parameters combined with weather forecast.
       
- email notifications

- alerts and internal notification system

- calendar displaying irrigations which has the possibility to add customizable events

- charts for displaying watering time

- search bar, for researches based on the city or the name of the area or garden.

Installation:
----- 

1. create and activate your virtual environment
2. Use the package manager pip to install Django 

    `pip install django`
3. Install requests modules
     
    `pip install requests`
3. clone git repository 
4. get into project folder
 
    `cd IrrigationApp`
6. Update db with initial data 

    `python manage.py migrate`
    
7. create a python file named mysettings and add 
   - secret key for your django app (you can generate one at [djecrety.ir](https://djecrety.ir/) )
   
      `SECRET_KEY = ''`
   - password for the gmail account used to send notifications (your account need to be set in the settings.py)
   
      `PASSWORD_GMAIL = '' `
   - ClimaCell API KEY
   
      `WEATHER_API_KEY = ' '`   
8. Run application

    `python manage.py runserver
`
