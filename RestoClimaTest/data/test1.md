## Generated Story 8588699640078111187
* Saludo
* GetWeather
    - utter_ask_weatherDate
* GetWeather{"weatherDate": "hoy"}
    - slot{"weatherDate": "hoy"}
    - utter_ask_city
* GetWeather{"city": "tenerife", "weatherDate": "hoy"}
    - slot{"weatherDate": "hoy"}
    - slot{"city": "tenerife"}
    - utter_on_it
* Despedida
    - utter_goodbye
    - export

