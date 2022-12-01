import os
import requests
from typing import Dict

from bs4 import BeautifulSoup


class VideoIsInvalid(Exception):
    pass

ServerUrl: str = "https://musicaldown.com/"
PostUrl: str = f"{ServerUrl}id/download"

Headers: Dict[str, str] = {
    "Host": "musicaldown.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers"
}

class TikTok:
    def __init__(self, url: str) -> None:
        self.url = url

        self.session = requests.Session()
        self.session.headers.update(Headers)

        self.request = self.session.get(ServerUrl)

    def download_video(self, filename: str) -> None:
        data = {}

        parse = BeautifulSoup(self.request.text, "html.parser")
        get_input = parse.findAll('input')

        for index in get_input:
            if index.get("id") == "link_url":
                data[index.get("name")] = self.url

            else:
                data[index.get("name")] = index.get("value")
        
        request_post = self.session.post(PostUrl, data=data, allow_redirects=True)

        if request_post.status_code == 302 \
        or "This video is currently not available" in request_post.text \
        or "Video is private or removed!" in request_post.text \
        or "Submitted Url is Invalid, Try Again" in request_post.text:

            raise VideoIsInvalid
        
        get_all_blank = BeautifulSoup(request_post.text,"html.parser").findAll(
            "a", attrs={"target": "_blank"})

        download_link = get_all_blank[0].get('href')
        get_content = requests.get(download_link)

        with open(filename, 'wb') as file:
            file.write(get_content.content)
            file.close()

            return os.path.join(filename)