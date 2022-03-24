import requests
from re import search
from time import time
from os import path, makedirs


def parse(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    response = requests.Session()
    rs = response.get(url=url, headers=headers)
    if rs.ok:
        re_expr = r"file: ['\"](.*?)['\"]"
        match = search(re_expr, rs.text)
        if match:
            video_url = match.group(1)
            rs = response.get(url=video_url, headers=headers)
            if rs.ok:
                filename = f"{url.split('/')[-1]}.mp4"
                with open(f'data/{filename}', 'wb') as video_file:
                    video_file.write(rs.content)
                return None
            else:
                return 'Не удалось перейти по ссылке с видео.'
        else:
            return 'Не удалось вытянуть ссылку на видео.'
    else:
        return 'Не удалось перейти на url'


def main():
    if not path.exists('data'):
        makedirs('data')
    url = input('Введите ссылку на видео: \n')
    start_time = time()
    res = parse(url=url)
    if res is None:
        print(f"--- {time() - start_time} секунд затрачено ---")
    else:
        print(res)


if __name__ == '__main__':
    main()
