## Indoor-localizer-iot-system 

IOT application to localize students in the SBME (systems and biomedical engineering) department real time using machine learning technique.


## Requirements 

ESP chip which is a microcontroller chip used to make wireless communication

## sequence 

  - ESP chip make wireless communication with server hosted by heroku to transfer wifi strength 
  - the strength of wifi is used as input for a machine learning model which is also hosted in a server at horoku.
  - the model predict the location and sent it to web page and mobile application at the same time to update location.
  - the location is updated on both the mobile application and web application real time as a moving point.
  - the application also provide a history to reshow the track it takes.
