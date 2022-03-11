/*
 * @Author: Ahmed Badra
 * @title: IOT application for collecting wifi connections' strengths labelled with certain location
 * @mcu: ESP8266
 */

#include <ESP8266WiFi.h>
#include "Dictionary.h"

/***************************** objects used in the applications ***********************/
Dictionary &strengths = *(new Dictionary(20));

/*
 * @brief: function to be executed once at the beginning of the program
 * @description: function that handles these tasks
 *              01. loop over wifi's networks' names 
 *                  a. create a new key for this network's strengths in the dictionary
 *                  b. if this network have already a key, ignore it
 *                  c. repeat this loop 5 times
 *              02. right now you have a dictionary containing some networks' names to fill in along the csv file
 *              03. print out dictionary keys (networks' names) into the csv file as a header (first row is the header)
 *              04. print out the last column name of the header as "location" to fill with the current location's label
 */
void setup() {
  /* setup the serial comm */
   Serial.begin(9600);
   Serial.println("clear the data now, I will wait 5 seconds for you");
   delay(5000);

   for(int i=0; i < 5; i++){
  /* repeat the below code 5 times */
     int n = WiFi.scanNetworks();
     /* loop over the networks */
     for (int i = 0; i < n; i++)
     {
        /* check if this network exist as a key in the idctionary or not */
        if(strengths(WiFi.SSID(i)) != true){
          /* this network's name not exist as a key, add it */         
          strengths(WiFi.SSID(i), -100);
        }
        /* this network name exist as a key, ignore it */
     }
   }
    /* print out the networks names (key of the dictionary) as a header (first row in the csv) */
    for(int i=0; i < strengths.count(); i++){
      Serial.print(strengths(i));
      Serial.print(',');      
    }
    /* print out the label at the end of the header row */
    Serial.print("location");
    Serial.println();
}

/* 
 *  @brief: function for periodic execution of the program
 *  @description: function that handles these tasks periodically
 *                01. loop over the networks strengths that the esp8266 currently read
 *                    a. if this network's name exist as a key, update it's value (strength value)
 *                    b. if not, ignore it as it's an a potential unstable network
 *                02. loop over the dictionary tuples
 *                    a. print out the current strength in order of networks' names
 *                03. print out the label value of the current location you are collecting from (check the Mapping in the server)
 *                04. refill all the strengths with zeros
 */
void loop() {
    /* update the dictionary values (strength values) by the new readings */
   int n = WiFi.scanNetworks();
   for (int i = 0; i < n; i++)
   {
      if(strengths(WiFi.SSID(i))){
        strengths(WiFi.SSID(i), WiFi.RSSI(i));
      }
   }

    /* print out dictionary values into the csv file */
   for(int i=0 ; i < strengths.count(); i++){
      Serial.print(strengths[i]);
      Serial.print(',');
   }
   /* print out the label you are filling in the csv for your current readings */
   Serial.print("HW 11");
/*   
   '3201 upper left':16, 
   '3201 upper right':1,
   '3201 lower left':2,
   '3201 lower right':3,
   'HW 11':4,
   'HW 12':5,
   'HW 21':6,
   'HW 22':7,
   'HW 23':8,
   'HW 31':9,
   'HW 32':10, ##
   'HW 33':11,
   'EL 11':12,
   'EL 12':13,
   'TAMER 11':14,
   'TA 11':15,
}
*/
   
   /* print out a \n for a new row insert */
   Serial.println();
    /* fill the dictionary by zero */
   for(int i=0 ; i < strengths.count(); i++){
      if(strengths(strengths(i)) == true){
        strengths(strengths(i), -100);
      }
   }
}
