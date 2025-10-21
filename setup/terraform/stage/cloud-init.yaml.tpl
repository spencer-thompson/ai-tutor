#cloud-config
users:
  - name: ubuntu
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - "${public_key}"

package_update: true
package_upgrade: true

write_files:
  - path: /usr/local/bin/bootstrap.sh
    owner: root:root
    permissions: '0755'
    content: |
${bootstrap}

runcmd:
  - [ /usr/local/bin/bootstrap.sh ]
  - [ sh, -c, 'echo "Provision complete" > /var/log/provision.log' ]
