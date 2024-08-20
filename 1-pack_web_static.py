#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the contents
of the web_static folder.
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: The path to the created archive, or None
    """
    # Define the archive directory and ensure it exists
    versions_dir = "versions"
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)

    # Generate the filename with a timestamp
    now = datetime.now()
    archive_name = f"web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"
    archive_path = os.path.join(versions_dir, archive_name)

    # Create the .tgz archive
    result = local(f"tar -cvzf {archive_path} web_static")

    if result.failed:
        return None
    return archive_path
