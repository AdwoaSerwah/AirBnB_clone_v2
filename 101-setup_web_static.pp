# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create /data directory
file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create /data/web_static directory
file { '/data/web_static':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create /data/web_static/releases directory
file { '/data/web_static/releases':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create /data/web_static/shared directory
file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create /data/web_static/releases/test directory
file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>",
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}
# Create or recreate the symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create the Nginx configuration file with custom header and redirection
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => @(END),
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        # Add custom header
        add_header X-Served-By $HOSTNAME;

        location /hbnb_static/ {
                alias /data/web_static/current/;
        }

        location / {
                try_files $uri $uri/ =404;
        }

        location /redirect_me {
                return 301 https://www.youtube.com/watch%3Fv%3DQH2-TGUlwu4;
        }

        error_page 404 /custom_404.html;
        location = /custom_404.html {
                internal;
        }
}
END
  mode    => '0644',
  owner   => 'root',
  group   => 'root',
  notify  => Service['nginx'],
}

# Ensure Nginx is running and enabled
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
