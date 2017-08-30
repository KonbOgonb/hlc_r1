# Start Gunicorn processes
echo Starting memcached.
/etc/init.d/memcached start
echo loading initial data
python3 dataImporter.py &
echo Starting gunicorn.
exec gunicorn app:app --bind 0.0.0.0:80 --workers=11 --keep-alive=5 --preload --timeout=30 --graceful-timeout=30 --backlog=4096