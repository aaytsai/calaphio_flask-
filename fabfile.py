from fabric.api import env
from fabric.operations import run, put

env.hosts = ['calaphio2@calaphio.com']

def deploy():
    # Transfer App
    put('calaphio', 'members2.calaphio.com')

    # Transfer Requirements
    put('requirements.txt', 'members2.calaphio.com')

    # Activate Source & Install Requirements
    run('source members2.calaphio.com/bin/activate && pip install -r members2.calaphio.com/requirements.txt')

    # Restart
    run('touch members2.calaphio.com/tmp/restart.txt')

def restart():
    run('touch members2.calaphio.com/tmp/restart.txt')
