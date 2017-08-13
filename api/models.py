import json
import requests
from django.db import models

# Create your models here.

class Gif(models.Model):

    urls = models.TextField()
    text = models.CharField(max_length=1024)

    @classmethod
    def get_gifs(cls, text):
        gifs = cls.objects.filter(text=text).values_list("urls", flat=True)

        if gifs:
            gif_urls = []
            for gif in gifs:
                gif_urls.extend(json.loads(gif))
            return gif_urls

        else:
            response = requests.get(
                   'https://api.gfycat.com/v1test/gfycats/search?search_text=%s&count=5' % text) 
            api_data = response.json()
            urls = [gif.get('max2mbGif') for gif in api_data.get('gfycats', [])]
            cls.objects.create(
                text=text,
                urls=json.dumps(urls)
            )
            return urls


    @classmethod
    def get_gif(cls, text, index):
        try:
            return cls.get_gifs(text)[index]
        except IndexError:
            return ''
