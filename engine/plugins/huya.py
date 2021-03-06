import base64
import html
import json
import requests

from engine.plugins import FFmpegdl, fake_headers, match1
from common import logger

VALID_URL_BASE = r'(?:https?://)?(?:(?:www|m)\.)?huya\.com'


class Huya(FFmpegdl):
    def __init__(self, fname, url, suffix='flv'):
        super().__init__(fname, url, suffix)

    def check_stream(self):
        logger.debug(self.fname)
        res = requests.get(self.url, timeout=5, headers=fake_headers)
        res.close()
        huya = match1(res.text, '"stream": "([a-zA-Z0-9+=/]+)"')
        if huya:
            huyajson = json.loads(base64.b64decode(huya).decode())['data'][0]['gameStreamInfoList'][0]
            absurl = u'{}/{}.{}?{}'.format(huyajson["sFlvUrl"], huyajson["sStreamName"], huyajson["sFlvUrlSuffix"], huyajson["sFlvAntiCode"])
            self.ydl_opts["absurl"] = html.unescape(absurl)
            return True


__plugin__ = Huya
