
/*
 * @Author: Ahmed Badra
 * @title: IOT application for updating the localizer website service with the current location's wifi networks' strengths
 * @mcu: ESP8266
 */

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>
#include "Dictionary.h"

/* server link */
const char *server_url = "http://python-server-model.herokuapp.com/";// Flask local application endpoint

/***************************** PROTOTYPES DECLARATIONS ********************************/
//void sendPOSTRequest(const char* server_url, const char* route, String urlencodedParams);
//void sendGETRequest(const char* server_url, const char* route);
void sendJSON(const char* server_url, const char* route, const char* json_str);


/***************************** objects used in the applications ***********************/
WiFiClient client;
HTTPClient http;
Dictionary &strengths = *(new Dictionary(20));

/*
 * @brief: function to be executed once at the beginning of the program
 */
void setup() {
  /* setup the serial Monitor and the DHT sensor connection then wait 3 seconds */
   Serial.begin(9600);
   delay(3000);

     /* get a list of the available active connections, print them on the serial monitor */
   uint8_t n = WiFi.scanNetworks();
   for(uint8_t i = 0; i < n; i++){
    Serial.print(i);
    Serial.print(". ");
    Serial.println(WiFi.SSID(i));
   }

   /* input the SSID name of the Network you want to connect to */
   Serial.print("enter the SSID name to connect with: ");
   while (Serial.available() == 0){ /* Wait for user input */ }  
   String ssid_name = Serial.readString();
   /* remove the \n in the end of the input */
   ssid_name[ssid_name.length() -1]  = '\0';
   Serial.println();   
   /* input the SSID Password of the Network you want to connect to */
   Serial.println("enter the password: ");
    while (Serial.available() == 0){ /* Wait for user input */ }
    String password = Serial.readString();
    /* remove \n in the end of the input */
    password[password.length() -1] = '\0';
    /* use the inputs (name, password) to connect to the Network */
   Serial.print(ssid_name + ",  " + password);
   WiFi.begin(ssid_name, password);
   /* poll over the connection successfully state of the WiFi module */
   while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
   }
   Serial.println("WiFi connected");
   delay(1000);
}

/* 
 *  @brief: function for periodic execution of the program
 */
void loop() {
    /* update the dictionary values (strength values) by the new readings */
   int n = WiFi.scanNetworks();
   for (int i = 0; i < n; i++)
   {
    /* insert that network's name and strength to the dictionary */
     strengths(WiFi.SSID(i), int(WiFi.RSSI(i)));
   }

    /* print out dictionary values as a json string in the serial monitor for debugging */
   Serial.print(strengths.json());

    /* send the json to the "rcvjson service in the server_url */
    sendJSON(server_url, "result", strengths.json().c_str());

   /* resetting the dictionary for the next loop refill with the current strengths */
    while ( strengths.count() ) strengths.remove(strengths(0));
}


/*
 * @brief: funcion that send a json string which is produced from a dictionary to a server_url in a specific route service
 */
void sendJSON(const char* server_url, const char* route, const char* dict_str){
  
    /* concatenate the server url with the target route service path */
    String service_url = String(server_url) + String(route);

    /* open a connection with this service in the server */
    http.begin(client, "http://python-server-model.herokuapp.com/result");

    /* set the datatype you will send */
    http.addHeader("Content-Type", "application/json");
    
    /* send the main data, which is the json string in this case */
    int httpCode = http.POST(dict_str);
    
    /* if there is a status code sent, get in the if statement */
    if(httpCode > 0){
      if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
    
          /* the data sent successfully, read the response and print it in the serial monitor */
          String payload = http.getString();
          Serial.println("Response: ");Serial.println(payload);
        }
    }else{
         /* the data transmission failed, print out the error code you received for debugging */
         Serial.printf("[HTTP] GET... failed, error: ");
         Serial.println(http.errorToString(httpCode).c_str());
    }
    
    /* close the connection */
    http.end(); 
}
