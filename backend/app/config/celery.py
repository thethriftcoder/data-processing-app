from celery import Celery


app = Celery("data_processor")
app.config_from_object("app.config.celeryconfig")
