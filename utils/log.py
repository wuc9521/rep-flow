import inspect

def log_(logger, level, message):
    cf = inspect.currentframe()
    caller_frame = cf.f_back
    caller_info = inspect.getframeinfo(caller_frame)
    log_message = f"{caller_info.filename}:{caller_info.lineno} - {message}"
    if level == 'info':
        logger.info(log_message)
    elif level == 'error':
        logger.error(log_message)
    elif level == 'warning':
        logger.warning(log_message)
    elif level == 'debug':
        logger.debug(log_message)
    else:
        raise ValueError(f"Unsupported log level: {level}")

