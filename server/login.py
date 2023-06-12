import os

def login(username, password):
    if username == 'rj1996' and password == 'yt2431':
        return {'status': 200, 'success': True}
    else:
        return {'status': 500, 'success': False}

