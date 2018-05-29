## greet
* Greet
    - utter_greet
    - reset_slots  

## Ask1
* Greet
    - utter_greet
    - reset_slots  
* GetWeather
    - utter_ask_loc
* GetWeather{"city": "London"}
    - action_show
> check_more_info
* Bye
    - utter_goodbye
    
> check_more_info
* GetWeather{"city": "London"}
    - action_show



## Ask2
* Greet
    - utter_greet
    - reset_slots  
* GetWeather{"city": "London"}
    - action_show
* Bye
    - utter_goodbye

## bye
* Bye
    - utter_goodbye

