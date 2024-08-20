#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx if it's not already installed
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get install -y nginx
fi

# Create required directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file to test Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create or recreate the symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content from /data/web_static/current/ to hbnb_static
if ! grep -q '^[^#]*location /hbnb_static/ {' "/etc/nginx/sites-available/default"; then
    sed -i '/^[^#]*location \/ {/i\\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}\n' /etc/nginx/sites-available/default
fi

# Restart Nginx to apply the changes
service nginx restart

# Exit successfully
exit 0
