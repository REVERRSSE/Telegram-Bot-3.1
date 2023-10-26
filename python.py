import requests
import time
import datetime
from pytz import all_timezones, timezone

token = "6152111660:AAGs-81mWjCl9WL3KA1MLNmrivyR5QqoQ9s"  # Replace with your bot's token
url = f"https://api.telegram.org/bot{token}/"

user_city = {}

def get_updates(offset=None):
    while True:
        try:
            response = requests.get(url + 'getUpdates', params={'timeout': 100, 'offset': offset})
            data = response.json()
            return data['result']
        except:
            time.sleep(1)

def send_message(chat_id, text):
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(url + 'sendMessage', params)
    return response

def find_timezone(city):
    city = city.lower().replace(" ", "_")
    for tz in all_timezones:
        if city in tz.lower():
            return tz
    return None

def get_time(city):
    tz = find_timezone(city)
    if tz is not None:
        now_time = datetime.datetime.now(timezone(tz))
        return now_time
    else:
        return None

def main():
    update_id = None
    while True:
        updates = get_updates(update_id)
        for update in updates:
            update_id = update['update_id'] + 1
            chat_id = update['message']['chat']['id']
            message_text = update['message']['text'].lower()

            if message_text == "/start":
                send_message(chat_id, "Welcome to the Time Zone Bot! Simply type the name of the city to get its current time. To get the time difference between your current city and another city, just type the name of the city. If you want to set your current city, type '/setcity your_city_name'.")
            elif message_text.startswith("/setcity"):
                try:
                    user_city[chat_id] = message_text.split("/setcity ", 1)[1]
                    send_message(chat_id, f"Your current city is set to {user_city[chat_id]}")
                except IndexError:
                    send_message(chat_id, "Please provide a city name after /setcity.")
            else:
                if chat_id in user_city:
                    city1_time = get_time(user_city[chat_id])
                    city2_time = get_time(message_text)
                    if city1_time is not None and city2_time is not None:
                        diff_hours = abs(city1_time.hour - city2_time.hour)
                        diff_minutes = abs(city1_time.minute - city2_time.minute)
                        send_message(chat_id, f"The time difference between {user_city[chat_id]} and {message_text} is {diff_hours} hours and {diff_minutes} minutes. The current time in {message_text} is {city2_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    else:
                        send_message(chat_id, "One or both cities are not in the timezone database. Please enter valid city names.")
                else:
                    city_time = get_time(message_text)
                    if city_time is not None:
                        send_message(chat_id, f"The current time in {message_text} is {city_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    else:
                        send_message(chat_id, f"Sorry, I couldn't find the timezone for {message_text}. Please enter a valid city name.")
        time.sleep(1)

if __name__ == "__main__":
    main()
