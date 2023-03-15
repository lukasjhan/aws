from inspect import currentframe, getframeinfo
import datetime

def get_log_info(cf):
  info = getframeinfo(cf.f_back)
  return info.filename, cf.f_back.f_lineno

def gen_msg(type, filename, line_number, msg):
  time = datetime.datetime.now()
  return f'[{type}]({filename}:{line_number}) [{time}] {msg}'

class Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]

def console_log(msg):
  print(msg)

def file_log(msg):
  if not hasattr(file_log, "coroutine"):
    file_log.coroutine = file_log_coroutine()
    next(file_log.coroutine)
  file_log.coroutine.send(msg)

def file_log_coroutine():
  time = datetime.datetime.now()
  with open(f'log-{time}.txt', 'a') as myfile:
    while True:
      msg = (yield)
      myfile.write(f'{msg}\n')

class Logger(object, metaclass=Singleton):
  def __init__(self, log_handlers=[console_log]):
    self.log_handlers = log_handlers

  def error(self, msg):
    filename, line_number = get_log_info(currentframe())
    self.__log__(gen_msg('ERROR', filename, line_number, msg))

  def warn(self, msg):
    filename, line_number = get_log_info(currentframe())
    self.__log__(gen_msg('WARN', filename, line_number, msg))

  def info(self, msg):
    filename, line_number = get_log_info(currentframe())
    self.__log__(gen_msg('INFO', filename, line_number, msg))

  def debug(self, msg):
    filename, line_number = get_log_info(currentframe())
    self.__log__(gen_msg('DEBUG', filename, line_number, msg))

  def __log__(self, msg):
    for handler in self.log_handlers:
      handler(msg)