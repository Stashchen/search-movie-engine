from api.forms import DEFAULT_MOVIES_FORM_INITIALS


def parse_movies_get_params(request):
    """
    Function, that prepare data for the django form
    
    :param request: Djagno WSGI request 

    :return: Parsed GET params
    """

    data = DEFAULT_MOVIES_FORM_INITIALS.copy()  # Get default data as the main source
    data.update({key: value for key, value in request.GET.items()})
    
    return data