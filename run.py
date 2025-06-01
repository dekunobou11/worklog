# run.py
from app import app
from config import DevelopmentConfig

if __name__ == '__main__':
    app.config.from_object(DevelopmentConfig)
    app.run(host='0.0.0.0', port=5001, debug=True)
