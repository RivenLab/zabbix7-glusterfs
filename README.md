# Zabbix GlusterFS

Monitor GlusterFS with Zabbix using `gstatus` and a Python helper script.

The script:
- Discovers Gluster volumes.
- Returns cluster values for Zabbix items.
- Returns per-volume values for Zabbix low-level discovery.

This project was updated for modern `gstatus` JSON output and Zabbix 7.x. The original project was made for older Zabbix versions.

#### Credits

Original project by MrCirca:

    https://github.com/MrCirca/zabbix-glusterfs

gstatus project:

    https://github.com/gluster/gstatus
---

## Requirements

Install on the **Gluster node** you want Zabbix to monitor:

- Python 3
- [gstatus](https://github.com/gluster/gstatus)
- Zabbix agent or Zabbix agent 2

`gstatus` must be run as root or with sudo because it calls the Gluster CLI internally.

## Install script

Copy the script to:

```bash
/usr/local/bin/gstatus_discovery.py
```
Make it executable:

```bash
chmod +x /usr/local/bin/gstatus_discovery.py
```
Sudo permission

### Open sudoers:

```bash
visudo /etc/sudoers.d/zabbix
```
Add this line:

```text
zabbix ALL=(root) NOPASSWD: /usr/local/bin/gstatus_discovery.py, /usr/local/bin/gstatus_discovery.py *
```
Use the full path.
### Zabbix agent config
#### Zabbix Agent 2

Create:

```bash
/etc/zabbix/zabbix_agent2.d/glusterfs.conf
```
#### Classic Zabbix agent

Create:

```bash
/etc/zabbix/zabbix_agentd.d/glusterfs.conf
```
Add:

```text
UserParameter=gluster_volume_name.discovery,sudo /usr/local/bin/gstatus_discovery.py
UserParameter=gluster_storage_info[*],sudo /usr/local/bin/gstatus_discovery.py "$1"
UserParameter=gluster_volume_info[*],sudo /usr/local/bin/gstatus_discovery.py "$1" "$2"
```
Zabbix user parameters are defined with UserParameter=<key>,<command>.

Restart the agent after saving:

```bash
systemctl restart zabbix-agent2
```

Agent include files and custom user parameters are supported by both agent and agent 2.
Test commands
Discover volumes

```bash
/usr/local/bin/gstatus_discovery.py
```
Example:

```json
{"data":[{"{#VOLUME_NAME}":"gfs"}]}
```
Get cluster value

```bash
/usr/local/bin/gstatus_discovery.py nodes_active
/usr/local/bin/gstatus_discovery.py usable_capacity
/usr/local/bin/gstatus_discovery.py used_capacity
/usr/local/bin/gstatus_discovery.py status
```
Example output:

```bash
3
21407727616
600784896
Healthy
```
Get volume value

```bash
/usr/local/bin/gstatus_discovery.py used_capacity gfs
/usr/local/bin/gstatus_discovery.py usable_capacity gfs
/usr/local/bin/gstatus_discovery.py state gfs
```
Example output:

```bash
600784896
21407727616
up
```
Use your real volume name, for example gfs.
Test with Zabbix agent

Test from the agent side before importing the template:

```bash
zabbix_agent2 -t gluster_volume_name.discovery
zabbix_agent2 -t 'gluster_storage_info[nodes_active]'
zabbix_agent2 -t 'gluster_storage_info[usable_capacity]'
zabbix_agent2 -t 'gluster_volume_info[used_capacity,gfs]'
zabbix_agent2 -t 'gluster_volume_info[state,gfs]'
```
These checks confirm that the UserParameters are loaded and working.
Import template

Import the custom Zabbix template YAML into Zabbix and link it to your Gluster host.

In Zabbix:

    Go to Data collection

    Open Templates

    Click Import

    Import the custom GlusterFS template

    Link it to your host

The GlusterFS community integration is listed by Zabbix as compatible with Zabbix 7.0+.
Notes

This project uses modern gstatus JSON field mapping:

    status -> cluster_status

    used_capacity -> size_used

    usable_capacity -> size_total

    state -> health

Some old fields from the original template were removed or adjusted because they are not present in current gstatus output.

### Troubleshooting
##### Permission denied

Make sure the zabbix user can run the script with sudo:

```bash
sudo -u zabbix sudo /usr/local/bin/gstatus_discovery.py nodes_active
```
---
