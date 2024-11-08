import multiprocessing

# Основные настройки
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = '-'  # Вывод логов доступа в stdout
errorlog = '-'   # Вывод логов ошибок в stdout
loglevel = 'debug'  # Уровень логирования
# accesslog = '/log/gunicorn_access.log'
# errorlog = '/log/gunicorn_error.log'

# Вариант для вывода логов в файл (если требуется)

