#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the contents
of the web_static folder.
"""

from fabric.api import local, run, env
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
        return False

    try:
        # Upload the archive to /tmp/
        put(archive_path, '/tmp/')

        # Extract the archive filename without extension
        arch_name = os.path.basename(archive_path)
        new_name = arch_name.split(".")[0]

        # Create the directory for the new_name release
        run('mkdir -p /data/web_static/releases/{}/'.format(new_name))

        # Uncompress the archive to the new_name directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            arch_name, new_name))

        # Delete the archive from the server
        run('rm /tmp/{}'.format(arch_name))

        # Move the contents of web_static to the release directory
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(new_name, new_name))

        # Remove the arch_name web_static directory
        run('rm -rf /data/web_static/releases/{}/web_static'.format(new_name))

        # Remove the arch_name symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new_name symbolic link
        run('ln -s /data/web_static/releases/{}/ '
            '/data/web_static/current'.format(new_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(e))
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
