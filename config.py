import os
from ytmusicapi import YTMusic


yt = YTMusic('browser.json', proxies={
    'http': os.environ['HTTP_PROXY'],
    'https': os.environ['HTTP_PROXY']
})
