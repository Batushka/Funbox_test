import math
from datetime import datetime
import json
from urllib.parse import urlparse
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework.response import Response

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


@api_view(['POST'])
def visited_links(request, *args, **kwargs):
    if request.method == 'POST':
        request_time = math.trunc(datetime.timestamp(datetime.now()))
        array = json.loads(request.body)
        key = list(array.keys())[0]
        values = array[key]
        pairs = {}
        for value in values:
            pairs[value] = request_time
        redis_instance.zadd("links", pairs)
        response = {
            "status": "ok",
        }

        return Response(response, 201)
    elif (request.method == 'PUT'
          or request.method == 'DELETE'):
        response = {
            "status": "method not allowed"
        }

        return Response(response, status=405)


@api_view(['GET'])
def visited_domains(request, *args, **kwargs):
    if request.method == 'GET':
        if request.query_params['from'] and request.query_params['to']:
            if ((request.query_params['from']).isdigit()
                    and (request.query_params['to']).isdigit()
                    and len(request.query_params['from']) == 10
                    and len(request.query_params['to']) == 10):
                domains = []
                links = redis_instance.zrangebyscore("links",
                                                     request.query_params['from'],
                                                     request.query_params['to'])
                for link in links:
                    if (('https://' not in str(link))
                            and ('http://' not in str(link))):
                        if '/' in str(link):
                            first_slash = str(link).find('/')
                            domain = link[:first_slash - 2]  # byte-string b'
                        else:
                            domain = link
                    else:
                        domain = urlparse(link).netloc
                    domains.append(domain)

                if not domains:
                    response = {
                        "status": "not found"
                    }
                    return Response(response, status=404)
                else:
                    unique_values = set(domains)
                    unique_domains = list(unique_values)

                    response = {
                        "domains": unique_domains,
                        "status": "ok"
                    }
                    return Response(response, status=200)
            else:
                response = {
                    "status": "bad request"
                }
                return Response(response, status=400)
    elif (request.method == 'POST'
          or request.method == 'PUT'
          or request.method == 'DELETE'):
        response = {
            "status": "method not allowed"
        }
        return Response(response, status=405)
