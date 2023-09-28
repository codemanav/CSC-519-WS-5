

## Sample `mysql` setup in ansible:

```
---
- name: Playbook to deploy MySQL Server and populate with data
  hosts: mysql_server
  become: yes
  become_method: sudo

  vars_prompt:
      - name: db_password
        prompt: 'Enter MySQL Password'
        private: yes # Hide user input (password)

  tasks:
      - name: install mysql-server
        apt:
            name: mysql-server
            update_cache: yes
            cache_valid_time: 3600
            state: present

      - name: Enable LOAD DATA LOCAL INFILE for MySQL Server
        shell: |
            echo "[mysqld]
            local_infile=1" >> /etc/mysql/my.cnf
      - name: Allow connections from outside localhost
        shell: |
            echo "bind-address=0.0.0.0" >> /etc/mysql/my.cnf
      - name: Restart MySQL service
        service:
            name: mysql
            state: restarted

      - name: Wait for MySQL service to fully restart
        wait_for:
            host: localhost
            port: 3306
        delay: 10
        timeout: 60

      - name: Create new mysql 'user' and set password
        shell: |
            mysql -u root -e "CREATE USER 'user'@'%' IDENTIFIED BY '{{ db_password }}';"
            mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'user'@'%';"
            mysql -u root -e "FLUSH PRIVILEGES;"
      - name: Create a new MySQL database
        shell: |
            mysql -u root -p'{{ db_password }}' -e "CREATE DATABASE IF NOT EXISTS pointsdb;"
      - name: Create a new MySQL table
        shell: |
            mysql -u root -p'{{ db_password }}' -e "CREATE TABLE IF NOT EXISTS pointsdb.points (x DOUBLE PRECISION,y DOUBLE PRECISION);"
      - name: Copy CSV file to the remote server
        copy:
            src: /ws5/rand-x-y-data.csv
            dest: /var/lib/mysql-files/rand-x-y-data.csv

      - name: Import data from CSV into MySQL
        shell: |
            mysql -u root -p'{{ db_password }}' pointsdb \
            -e "LOAD DATA INFILE '/var/lib/mysql-files/rand-x-y-data.csv' INTO TABLE points FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES;"
      - name: Expose port 3306 with iptables
        shell: 'sudo iptables -I INPUT -p tcp -m tcp --dport 3306 -j ACCEPT'
```


