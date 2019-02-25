from app import app
from flask_script import Manager, Server
import os


manager = Manager(app)

manager.add_command('server', Server(host=os.getenv('APP_HOST', 'localhost'),
                                     port=int(os.getenv('APP_PORT', 5000))))


if __name__ == '__main__':
    manager.run()