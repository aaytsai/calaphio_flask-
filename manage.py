from flask_script import Shell, Manager

from calaphio import create_app

manager = Manager(create_app)
manager.add_command("shell", Shell())

if __name__ == "__main__":
    manager.run()