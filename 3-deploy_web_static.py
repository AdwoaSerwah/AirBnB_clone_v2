#!/usr/bin/python3
from fabric.api import local, put, run, env
from datetime import datetime
import os

env.hosts = ['100.25.177.89', '100.25.188.96']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Creates a .tgz archive from the web_static folder."""
    try:
        now = datetime.now()
        archive_name = 'versions/web_static_{}.tgz'.format(
                now.strftime('%Y%m%d%H%M%S'))
        local('mkdir -p versions')
        local('tar -cvzf {} web_static'.format(archive_name))
        return archive_name
    except Exception as e:
        print("Failed to pack archive: {}".format(e))
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not os.path.exists(archive_path):
        print("Path does not exist!")
        return False

    try:
        arch_name = os.path.basename(archive_path)
        new_name = arch_name.split(".")[0]
        the_path = "/data/web_static/releases/"

        # Upload the archive to the server
        put(archive_path, '/tmp/')

        # Create the directory for the new release
        run('mkdir -p {}{}/'.format(the_path, new_name))

        # Uncompress the archive to the new directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(arch_name, the_path, new_name))

        # Delete the archive from the server
        run('rm /tmp/{}'.format(arch_name))

        # Move the contents of web_static to the release directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(the_path, new_name))

        # Remove the old web_static directory
        run('rm -rf {}{}/web_static'.format(the_path, new_name))

        # Remove the old symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new release
        run('ln -s {}{}/ /data/web_static/current'.format(the_path, new_name))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Failed to deploy: {}".format(e))
        return False


def deploy():
    """Create and deploy an archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
