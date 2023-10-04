#!/bin/bash

# Define the list of playbooks to execute in order
playbooks=("0-update-security.yaml" "1-setup-config.yaml" "2-setup-config.yaml")

# Define the inventory file
inventory_file="hosts.yaml"

# Loop through the playbooks and run them
for playbook in "${playbooks[@]}"
do
    echo "Running playbook: $playbook"
    ansible-playbook -i "$inventory_file" "$playbook"
done
