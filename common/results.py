# -*-coding:utf-8-*-


def returnCode(code):
    """
    param code, return json
    """
    context = {}
    if code == 101:
        context = {
            'code': 101,
            'message': 'login success',
        }
    elif code == 102:
        context = {
            'code': 102,
            'message': 'error in username or password',
        }
    elif code == 103:
        context = {
            'code': 103,
            'message': 'username or password is null',
        }
    elif code == 104:
        context = {
            'code': 104,
            'message': 'registration error',
        }
    elif code == 105:
        context = {
            'code': 105,
            'message': 'registration success',
        }
    elif code == 106:
        context = {
            'code': 106,
            'message': 'username already exists',
        }
    elif code == 107:
        context = {
            'code': 107,
            'message': 'save user exception, please contact manager',
        }
    elif code == 108:
        context = {
            'code': 108,
            'message': 'friend information exception',
        }
    elif code == 109:
        context = {
            'code': 109,
            'message': 'friend information success',
        }
    elif code == 111:
        context = {
            'code': 111,
            'message': 'user information exception',
        }
    elif code == 112:
        context = {
            'code': 112,
            'message': 'quasi through success',
        }
    elif code == 113:
        context = {
            'code': 113,
            'message': 'quasi refused success',
        }
    elif code == 114:
        context = {
            'code': 114,
            'message': 'quasi operating error',
        }
    elif code == 115:
        context = {
            'code': 115,
            'message': 'edit my head photo success',
        }
    elif code == 116:
        context = {
            'code': 116,
            'message': 'edit my head photo error',
        }
    elif code == 117:
        context = {
            'code': 117,
            'message': 'edit my password error',
        }
    elif code == 118:
        context = {
            'code': 118,
            'message': 'old password error in edit my password',
        }
    elif code == 119:
        context = {
            'code': 119,
            'message': 'edit my password success',
        }
    else:
        context = {
            'code': 999,
            'message': 'system error!!! please contact manager, 3Q',
        }
    return context
