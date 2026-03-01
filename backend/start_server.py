import sys
import os
import traceback

print('Python version:', sys.version)
print('Current directory:', os.getcwd())
print('Files in current directory:', os.listdir('.'))

try:
    from app import app
    print('App created successfully')
    print('Starting server...')
    app.run(debug=True)
except Exception as e:
    print('Error starting server:', e)
    print('Traceback:')
    traceback.print_exc()
