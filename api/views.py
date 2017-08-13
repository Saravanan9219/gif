from rest_framework.decorators import api_view
from rest_framework.response import Response

import json

from api.models import Gif

# Create your views here.


def get_response_data(text, url, page, previous_page, next_page, in_channel=False):
    data = {
        'title': text,
        'attachments': [{
            'fallback': text,
            'image_url': url,
            'callback_id': page,
            'actions': [
                {
                    "name": "action",
                    "text": "Prev",
                    "type": "button",
                    "value": text + ';' + str(previous_page)
                },
                {
                    "name": "action",
                    "text": "Next",
                    "type": "button",
                    "value": text + ';' + str(next_page)
                },
                {
                    "name": "action",
                    "text": "Post",
                    "type": "button",
                    "value": text + ';post'
               }
            ]
        }],
    }
    if in_channel:
       data['replace_original'] = False
       data['delete_original'] = True
       data['response_type'] = 'in_channel'
       data['attachments'][0]['actions'] = [] 
    else:
       data['response_type'] = 'ephemeral'
    return data


@api_view(['POST',])
def get_gif(request):

    if 'payload' in request.data:
        payload = json.loads(request.data.get('payload'))
        action = payload.get('actions')[0]
        value = action.get('value', '').split(';')
        if value[-1] == 'post':
            page = int(payload.get('callback_id'))
            in_channel = True
            text_and_page = [value[0], str(page)]
        else:
            in_channel = False
            text_and_page = action.get('value', '').split(';')

    else:
        in_channel = False
        text_and_page = request.data.get('text', '').split(';')

    text = text_and_page[0]
    if len(text_and_page) > 1 and text_and_page[-1].isdigit():
        page = int(text_and_page[1])
    else:    
        page = 1
    
    url = Gif.get_gif(text, page - 1)
    total_pages = len(Gif.get_gifs(text))
    previous_page = page - 1 if page > 1 else total_pages 
    next_page = page + 1 if page < total_pages else 1
    data = get_response_data(text, url, page, previous_page, next_page, in_channel=in_channel)
    return Response(data=data)
