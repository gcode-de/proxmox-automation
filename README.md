# Proxmox Cluster Automation

Ansible playbooks for managing Proxmox cluster configuration.

## Setup

1. Install Ansible:
```bash
   apt install ansible
```

2. Configure SSH keys for passwordless access:
```bash
   ssh-keygen -t ed25519
   for ip in 211 212 213 216 217; do
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
ansible-playbook playbooks/nfs-mounts.yml --check

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

## Adding new NFS mounts

Edit `inventory/group_vars/proxmox_cluster.yml` and add to `nfs_mounts` list.
