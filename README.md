# Proxmox Cluster Automation

Ansible playbooks for managing Proxmox cluster configuration.

## Setup

1. Install Ansible:
```bash
   apt install ansible
   ansible-galaxy collection install -r collections/requirements.yml
```

2. Configure SSH keys for passwordless access:
```bash
   ssh-keygen -t ed25519
   for ip in 211 212 213 214; do
     ssh-copy-id root@192.168.68.$ip
   done
```

3. Test connectivity:
```bash
   ansible proxmox_cluster -m ping
```

## Usage

### Configure NFS mounts
```bash
ansible-playbook playbooks/nfs-mounts.yml

# Dry-run (check mode)
ansible-playbook playbooks/nfs-mounts.yml --check --diff

# Verbose output
ansible-playbook playbooks/nfs-mounts.yml -v
```

### Run on specific host
```bash
ansible-playbook playbooks/nfs-mounts.yml --limit pve1
```

## Inventory Structure

- `inventory/hosts.yml` - Host definitions
- `inventory/group_vars/proxmox_cluster.yml` - Cluster-wide variables
- `inventory/host_vars/` - Additional mounts for individual nodes
- `collections/requirements.yml` - Required Ansible collections

## Adding new NFS mounts

Add mounts required on every node to `nfs_mounts` in
`inventory/group_vars/proxmox_cluster.yml`. Add node-specific mounts to
`nfs_host_mounts` in `inventory/host_vars/<hostname>.yml`.

The default mount options use `nofail` and a 30-second systemd mount timeout,
so a temporarily unavailable NAS does not prevent a Proxmox node from booting.
