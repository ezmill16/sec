import requests
from bs4 import BeautifulSoup
import time

most_recent = "Lorem"

bot_token = '6737358620:AAE4VYxBDtyipTFPHGRAxXhmiBpvOkpOWgY'
channel_id = '@thesecinsider'  # Replace with your actual channel username or ID

def send_message(text):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {'chat_id': channel_id, 'text': text}
    response = requests.post(url, params=params)
    return response.json()

while True:
    time.sleep(1)
    page_to_scrape = requests.get("http://openinsider.com/latest-insider-trading")
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
    rows = soup.findAll("tr")

    row = rows[34]
    td = row.findAll("td")

    trade_type = ""

    if td:
        date_td = td[2].find("div")
        if date_td.text != most_recent:
            most_recent = date_td.text
            if td[7].text == "S - Sale":
                trade_type = "🔴"
            else:
                trade_type="🟢"

            if td[7].text == "S - Sale" or td[7].text == "P - Purchase":
                message = (
                    f"Trade Date: {date_td.text}\n\n"
                    f"Ticker: {td[3].find('b').find('a').text}\n\n"
                    f"Company: {td[4].find('a').text}\n\n"
                    f"Name: {td[5].find('a').text}\n\n"
                    f"Comp Title: {td[6].text}\n\n"
                    f"Trade Type: {td[7].text + trade_type}\n\n"
                    f"Price: {td[8].text}\n\n"
                    f"Qty: {td[9].text}\n\n"
                    f"Share Value: {td[12].text}\n\n"
                )
                send_message(message)
