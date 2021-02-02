import requests
from urllib.parse import urljoin

from django.conf import settings


def get_es_object_id(es_index: str, query_params: dict) -> str:
    """
    :param es_index:  ElasticSearch index
    :param query_params:  Dictionary that stores data for search request

    :return: ElasticSearch object _id
    """
    
    search_params = {
        'query': {
            'match': query_params
        }
    }

    response = requests.get(
        url=urljoin(settings.BASE_ES_URL, f'{es_index}/_search'),
        json=search_params,
        headers={'Content-Type': 'application/json'}
    ).json()

    return response['hits']['hits'][0]['_id']
    

def get(es_index: str, request_data: dict) -> requests.Response:
    """
    :param es_index:  ElasticSearch index
    :param request_data:  Data, that will be sent to ElasticSearch

    :return: ElasticSearch response
    """
    return requests.get(
      url=urljoin(settings.BASE_ES_URL, f'{es_index}/_search'),
      json=request_data,
      headers={'Content-Type': 'application/json'}
   )  

def post(es_index: str, request_data: dict) -> requests.Response:
    """
    :param es_index:  ElasticSearch index
    :param request_data:  Data, that will be sent to ElasticSearch

    :return: ElasticSearch response
    """
    return requests.post(
        url=urljoin(settings.BASE_ES_URL, f'{es_index}/_doc'),
        json=request_data,
        headers={'Content-Type': 'application/json'}
    )

def put(es_index: str, request_data: dict, es_id: str) -> requests.Response:
    """
    :param es_index:  ElasticSearch index
    :param request_data:  Data, that will be sent to ElasticSearch
    :param es_id:  id of updated data

    :return: ElasticSearch response
    """
    request_params = {
        'doc': request_data
    }

    return requests.post(
        url=urljoin(settings.BASE_ES_URL, f'{es_index}/_doc/{es_id}/_update'),
        json=request_params,
        headers={'Content-Type': 'application/json'}
    )

def delete(es_index: str, request_data: dict, es_id: str) -> requests.Response:
    """
    :param es_index:  ElasticSearch index
    :param request_data:  Data, that will be sent to ElasticSearch
    :param es_id:  id of updated data

    :return: ElasticSearch response
    """  
    return requests.delete(
        url=urljoin(settings.BASE_ES_URL, f'{es_index}/_doc/{es_id}'),
        json=request_data,
        headers={'Content-Type': 'application/json'}
    )