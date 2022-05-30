INSTALLED_APPS = [
    'channels',
    
    'some_app',
]


# Channels
ASGI_APPLICATION = 'main_app.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
