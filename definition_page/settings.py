try:
    from local_settings import *  # noqa: F401,F403
except ImportError as e:
    print('Import from local_settings failed, %s' % e)
