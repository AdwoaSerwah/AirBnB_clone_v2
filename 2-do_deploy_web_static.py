#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the contents
of the web_static folder and deploy it to the web servers.
"""

from fabric.api import local, run, env, put
from datetime import datetime
import os

env.hosts = ['100.25.177.89', '100.25.188.96']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'
executed_locally = False


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    """
    global executed_locally

    if not os.path.exists(archive_path):
        print("Path does not exist!")
        return False

    try:
        arch_name = os.path.basename(archive_path)
        new = arch_name.split(".")[0]
        the_path = "/data/web_static/releases/"

        # Only execute this block once locally
        if not executed_locally:
            local(f'cp {archive_path} /tmp/')
            local('mkdir -p {}{}/'.format(the_path, new))
            local('tar -xzf /tmp/{} -C {}{}/'.format(arch_name, the_path, new))
            local('rm /tmp/{}'.format(arch_name))
            local('mv {0}{1}/web_static/* {0}{1}/'.format(the_path, new))
            local('rm -rf {}{}/web_static'.format(the_path, new))
            local('rm -rf /data/web_static/current')
            local('ln -s {}{}/ /data/web_static/current'.format(the_path, new))
            executed_locally = True

        # Remote operations
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(the_path, new))
        run('tar -xzf /tmp/{} -C {}{}/'.format(arch_name, the_path, new))
        run('rm /tmp/{}'.format(arch_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(the_path, new))
        run('rm -rf {}{}/web_static'.format(the_path, new))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(the_path, new))

        return True
    except Exception as e:
        print("An error occurred:", e)
        return False


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static farch_nameer.

    Returns:
        str: The path to the created archive, or None
    """
    # Define the archive directory and ensure it exists
    versions_dir = "versions"
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)

    # Generate the filename with a timestamp
    now = datetime.now()
    arch_name = f"web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"
    archive_path = os.path.join(versions_dir, arch_name)

    # Create the .tgz archive
    result = local(f"tar -cvzf {archive_path} web_static", capture=True)

    if result.failed:
        return None
    return archive_path
