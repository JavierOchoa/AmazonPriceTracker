import requests
import schedule
from bs4 import BeautifulSoup
import smtplib
import time
import lxml

current_price = 90

TO_EMAIL = ''
FROM_EMAIL = ''
PASSWORD = ''
URL = 'https://www.amazon.com/-/es/dp/B0143UM4TC/?coliid=I2UQ5B6SPA0MB&colid=33GXE8XEPRG99&psc=1&ref_=lv_ov_lig_dp_it'
HEADERS = {
    'Request Line': 'GET / HTTP/1.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59'
}


def job():
    global current_price
    response = requests.get(url=URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "lxml")
    title = soup.find(name="span", id="productTitle").get_text().strip()
    price_text = soup.find(name="span", id="priceblock_ourprice").get_text().replace("\xa0", " ")
    price = float(price_text.split()[1])

    if price < current_price:
        message = f'{title} has a new price of ${price}'
        print(message)
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(FROM_EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=FROM_EMAIL,
                to_addrs=TO_EMAIL,
                msg=f"Subject:Amazon Low Price Alert! :)\n\n{message}\n\n{URL}")
        current_price = price

    elif price > current_price:
        message = f'{title} has a new price of ${price}'
        print(message)
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(FROM_EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=FROM_EMAIL,
                to_addrs=TO_EMAIL,
                msg=f"Subject:Amazon High Price Alert! :(\n\n{message}\n{URL}")
        current_price = price


schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
