import os
import requests
import argparse
from dotenv import load_dotenv
from urllib.parse import urlsplit


def shorten_link(token, url):
    header = {"Authorization": f"Bearer {token}"}
    payload = {"long_url": url}
    user_url = 'https://api-ssl.bitly.com/v4/bitlinks'

    response = requests.post(user_url, headers=header, json=payload)
    response.raise_for_status()
    short_link = response.json().get('id')
    return short_link


def count_clicks(token, link):
    split_link = urlsplit(link)
    link = f'{split_link.netloc}{split_link.path}'
    header = {"Authorization": f"Bearer {token}"}
    user_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'

    response = requests.get(user_url, headers=header)
    response.raise_for_status()
    total_clicks = response.json().get('total_clicks')
    return total_clicks


def is_bitlink(link, token):
    split_link = urlsplit(link)
    link = f'{split_link.netloc}{split_link.path}'
    header = {"Authorization": f"Bearer {token}"}
    user_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'

    response = requests.get(user_url, headers=header)
    return response.ok


if __name__ == '__main__':
    load_dotenv('data.env')
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(description='enter your url http://...')
    parser.add_argument('url', metavar='url', type=str, help='enter your url: ')
    args = parser.parse_args()
    url = args.url
    try:
        if is_bitlink(url, token):
            total_clicks = count_clicks(token, url)
            print('Total clicks: ', total_clicks)
        else:
            short_link = shorten_link(token, url)
            print('Your link: ', short_link)
    except requests.exceptions.HTTPError as e:
        print('HTTP Error: ', e)