import os
import requests
from bs4 import BeautifulSoup


class VideoIsInvalid(Exception):
    """Exception for invalid videos."""
    pass

class TikTok:
    """
    TikTok class.
    
    Parameters
    ----------
    url: :class:`str`
        TikTok video link.
    """
    def __init__(self, url: str) -> None:
        self.url = url
        self.headers = {
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

        self.server_url = "https://musicaldown.com/"
        self.post_url = self.server_url + "id/download"

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        self.request = self.session.get(self.server_url)
    
    def download_video(self, filename: str) -> str:
        """
        Video download method.
        
        Parameters
        ----------
        filename: :class:`str`
            Specify filename.
            
        Returns
        -------
        :class:`str`
            Path to the downloaded file.
        """
        data = {}

        parse = BeautifulSoup(self.request.text, "html.parser")
        get_input = parse.findAll('input')

        for index in get_input:
            if index.get("id") == "link_url":
                data[index.get("name")] = self.url

            else:
                data[index.get("name")] = index.get("value")
        
        request_post = self.session.post(self.post_url, data=data, allow_redirects=True)

        if request_post.status_code == 302 \
        or "This video is currently not available" in request_post.text \
        or "Video is private or removed!" in request_post.text \
        or "Submitted Url is Invalid, Try Again" in request_post.text:
            raise VideoIsInvalid("Video is invalid!")
        
        get_all_blank = BeautifulSoup(request_post.text,"html.parser").findAll(
            "a", attrs={"target": "_blank"})

        download_link = get_all_blank[0].get('href')
        get_content = requests.get(download_link)

        with open(filename, 'wb') as file:
            file.write(get_content.content)

        return os.path.join(os.getcwd(), filename)
