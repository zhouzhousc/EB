cd ..
cd tasks
cd edgebox_web
celery -A celery_tasks.tasks -l info worker -P eventlet