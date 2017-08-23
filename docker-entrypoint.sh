# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn app:app \
    --bind 0.0.0.0:80 \
    --workers 3 \