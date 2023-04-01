import requests


def get_requests_handler(url, headers={}, params={}, timeout=30):
    try:
        response = requests.get(url=url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        return {"status": "HTTPError", "info": errh}
    except requests.exceptions.ConnectionError as errc:
        return {"status": "ConnectionError", "info": errc}
    except requests.exceptions.Timeout as errt:
        return {"status": "Timeout", "info": errt}
    except requests.exceptions.RequestException as err:
        return {"status": "RequestException", "info": err}
    return {"status": "success", "info": response.text}


def post_requests_handler(url, headers={}, json={}, params={}):
    try:
        response = requests.post(url=url, headers=headers, json=json, params=params, timeout=30)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        return {"status": "HTTPError", "info": errh}
    except requests.exceptions.ConnectionError as errc:
        return {"status": "ConnectionError", "info": errc}
    except requests.exceptions.Timeout as errt:
        return {"status": "Timeout", "info": errt}
    except requests.exceptions.RequestException as err:
        return {"status": "RequestException", "info": err}
    return {"status": "success", "info": response.text}
