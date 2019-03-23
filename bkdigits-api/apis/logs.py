import logging


def err_logged(fn, msg=''):
    def decorate(*args, **kwargs):
        logger = logging.getLogger('flask.error')
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.exception(msg, exc_info=True)
            raise e
    return decorate
