import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
limit_request_fields = 100
limit_request_field_size = 8190
raw_env = 'DJANGO_SETTINGS_MODULE=web.settings.dev'

