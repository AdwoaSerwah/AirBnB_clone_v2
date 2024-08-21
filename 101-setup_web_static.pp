# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create required directories
file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create a fake HTML file to test Nginx configuration
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

# Ensure ownership of /data is set correctly
exec { 'change_ownership':
  command => 'chown -R ubuntu:ubuntu /data/',
  path    => ['/usr/bin', '/bin'],
  unless  => 'test $(stat -c "%U:%G" /data) = "ubuntu:ubuntu"',
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  content => epp('nginx/default.epp'),
  notify  => Service['nginx'],
}

# Restart Nginx to apply changes
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
