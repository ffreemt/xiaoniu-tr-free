r'''
xiaoniu translate for free

# pylint: disable=unused-import, unused-argument
'''
# pylint: disable=too-many-branches

import logging
from pathlib import Path
from time import sleep, time
from random import random, randint
from typing import Tuple

from urllib.parse import urlencode
import requests
import requests_cache  # type: ignore
# import langid  # type: ignore
from langid import classify  # type: ignore

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# for ipython copy-n-paste test
if '__file__' not in globals():
    __file__ = 'ipython_sessioin.py'

HOME_FOLDER = Path.home()
CACHE_NAME = (Path(HOME_FOLDER) / (Path(__file__)).stem).as_posix()
EXPIRE_AFTER = 36000

URL0 = "https://test.niutrans.vip"
URL0 = "https://niutrans.com/Trans"
REFERER = 'https://niutrans.vip/console/textTrans'
URL = 'http://api.niutrans.vip/NiuTransServer/translation'
URL = 'https://test.niutrans.com/NiuTransServer/testtrans'


UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17'  # NOQA
HEADERS = {
    "Origin": URL0,
    "User-Agent": UA,
    'Referer': REFERER,
}
HEADERS = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Dnt': '1',
    'Origin': 'https://niutrans.com',
    'Sec-fetch-site': 'same-site',
    'Sec-fetch-mode': 'cors',
    'Sec-fetch-dest': 'empty',
    'Referer': 'https://niutrans.com/Trans',
    'Accept-encoding': 'gzip, deflate, br',
    'Accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

# APIKEY = "918b7750dab1c9ec418dce28542d707a"

SESS = requests_cache.CachedSession(
    cache_name=CACHE_NAME,
    expire_after=EXPIRE_AFTER,
    allowable_methods=('GET', 'POST'),
)
SESS_T = requests_cache.CachedSession(
    cache_name=CACHE_NAME,
    expire_after=EXPIRE_AFTER,
    allowable_methods=('GET', 'POST'),
)


def make_throttle_hook(timeout=1):
    r"""
    Returns a response hook function which sleeps for `timeout` seconds if
    response is not cached

    time.sleep(min(0, timeout - 0.5) + random())
        average delay: timeout

    s = requests_cache.CachedSession()
    s.hooks = {'response': make_throttle_hook(0.1)}
    s.get('http://httpbin.org/delay/get')
    s.get('http://httpbin.org/delay/get')
    """
    def hook(response, *args, **kwargs):  # pylint: disable=unused-argument
        if not getattr(response, 'from_cache', False):
            # print(f'sleeping {timeout} s')

            timeout0 = min(0, timeout - 0.5) + random()
            LOGGER.debug('sleeping %s', timeout0)

            sleep(timeout0)
        return response
    return hook


THROTTLE_TIME = 0.67  # 1/.67 times/sec
EXEMPTED = 200

SESS_T.hooks = {'response': make_throttle_hook(THROTTLE_TIME)}

SESS_T.get(URL0)
SESS.get(URL0)


def xiaoniu_tr(
        query: str,
        from_lang: str = 'auto',
        to_lang: str = 'zh',
        timeout: Tuple[int, int] = (55, 66),
) -> str:
    '''
    xiaoniu_tr

    >>> xiaoniu_tr('test')
    '测试'
    >>> xiaoniu_tr('Good morning', to_lang='de')
    'Guten Morgen'
    >>> xiaoniu_tr('hello world', to_lang='fr')
    'Bonjour le monde'
    >>> xiaoniu_tr('hello world', to_lang='ru')
    'Привет, мир'
    >>> xiaoniu_tr('hello world', to_lang='ja')
    'こんにちは世界'
    '''

    from_lang = from_lang.lower()
    to_lang = to_lang.lower()

    if from_lang in ['auto']:
        # from_lang = langid.classify(query)[0]
        from_lang = classify(query)[0]
    if from_lang == to_lang:
        xiaoniu_tr.json = {'msg': 'from_lang == to_lang, nothing to do'}  # type: ignore  # NOQA
        return query

    # tick = round(time() * 1000)
    # will spoil cache
    data = {
        "query": 50980349,
        "source": "text",
        'from': from_lang,
        'to': to_lang,
        'src_text': query,
        # 't': tick,
        # 'apikey': APIKEY,
    }

    # is it the first EXEMPTED calls?
    try:
        xiaoniu_tr.counter += 1  # type: ignore
    except Exception:
        xiaoniu_tr.counter = 1  # type: ignore
    finally:
        if xiaoniu_tr.counter > EXEMPTED:  # type: ignore
            xiaoniu_tr.counter = EXEMPTED  # type: ignore
    if xiaoniu_tr.counter < EXEMPTED:  # type: ignore
        sess = SESS
    else:
        # throttle or not
        atime = time()
        if atime - xiaoniu_tr.atime < THROTTLE_TIME:  # type: ignore
            sess = SESS_T
        else:
            sess = SESS

    try:
        _ = """  # for some weird reason, post returns incoheret results
        resp = sess.post(
            URL,
            data=data,
            headers=HEADERS,
            timeout=timeout,
        )
        # """
        resp = sess.get(
            f"{URL}?{urlencode(data)}",
            headers=HEADERS,
            timeout=timeout,
        )
    except Exception as exc:
        LOGGER.error(exc)
        # resp.json = {"error_msg": str(exc)}
        resp = requests.models.Response()
        resp._content = f'{{"errorCode": "{exc}"}}'.encode()
        resp.status_code = 499

    try:
        jdata = resp.json()
    except Exception as exc:
        jdata = {'error_msg': str(exc)}
    finally:
        resu = jdata.get('tgt_text')

    xiaoniu_tr.json = jdata  # type: ignore

    # record exit timestamp
    xiaoniu_tr.atime = time()  # type: ignore

    if jdata.get('error_msg'):
        error_msg = jdata.get('error_msg')
        error_msg = f'{error_msg}: probably because <{from_lang}>-><{to_lang}> is not supported'  # NOQA
        LOGGER.error(error_msg)
        # raise Exception(error_msg)
        return ''

    return resu.strip()


def main():
    '''main'''
    import sys

    if not sys.argv[1:]:
        print('Provide something for the test.')
        print('Generating some random tests')

    query = ' '.join(sys.argv[1:]) or 'test ' + str(randint(0, sys.maxsize))
    res1 = xiaoniu_tr(query)
    res2 = xiaoniu_tr(query, 'en', 'de')

    print(f'query: {query}')
    print(f'to English: {res1}')
    print(f'to German: {res2}')


if __name__ == '__main__':
    main()
