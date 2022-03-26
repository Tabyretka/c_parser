import requests
from re import search
from time import time
from os import path, makedirs
import sys


def progress(count, total, status='', bar_len=60):
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    fmt = '[%s] %s%s ...%s' % (bar, percents, '%', status)
    print('\b' * len(fmt), end='')
    sys.stdout.write(fmt)
    sys.stdout.flush()


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
            rs = response.get(url=video_url, headers=headers, stream=True)
            if rs.ok:
                filename = f"{url.split('/')[-1]}.mp4"
                with open(f'data/{filename}', 'wb') as video_file:
                    total_length = int(rs.headers.get('content-length'))
                    for chunk in enumerate(rs.iter_content(chunk_size=1024 * 1024)):
                        if chunk[1]:
                            progress(chunk[0] * 1024 * 1024, total_length, status='скачивание')
                            video_file.write(chunk[1])
                    print(f'\nсохранено data/{filename}')


def main():
    if not path.exists('data'):
        makedirs('data')
    url = input('Введите ссылку на видео: \n')
    start_time = time()
    r = parse(url=url)
    if r is None:
        print(f"\n--- {time() - start_time} секунд затрачено ---")
    else:
        print(r)


if __name__ == '__main__':
    main()
