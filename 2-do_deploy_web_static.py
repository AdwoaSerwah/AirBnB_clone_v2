#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the contents
of the web_static folder.
"""

from fabric.api import local, run, env, put
from datetime import datetime
import os

env.hosts = ['100.25.177.89', '100.25.188.96']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    """
    if not os.path.exists(archive_path):
        print("Path does not exist!")
        return False

    try:
        result = put(archive_path, '/tmp/')
        # print("Put result:", result.succeeded)
        arch_name = os.path.basename(archive_path)
        new_name = arch_name.split(".")[0]
        the_path = "/data/web_static/releases/"
        run('mkdir -p {}{}/'.format(the_path, new_name))
        run('tar -xzf /tmp/{} -C {}{}/'.format(arch_name, the_path, new_name))
        run('rm /tmp/{}'.format(arch_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(the_path, new_name))
        run('rm -rf {}{}/web_static'.format(the_path, new_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(the_path, new_name))
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
