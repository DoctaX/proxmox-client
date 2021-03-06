
# Proxmox (PVE) API Client

I wanted a simple way to be able to pull down Proxmox node and vm metrics and so I wrote this CLI application using the Proxmoxer library which interfaces with the Proxmox API<br>
This script can be used to connect to a proxmox instance to retrieve a range of data regarding vm's

### Use cases
* Return a CSV file (e.g. excel) including a list of vm's and relevant information about them
* Return a YAML file that features a hierarchical list of nodes and vm's that an automation script (e.g. an ansible play) can hook into  

### Pre-requisites
* A PVE user account that has sufficient permissions to access VM data
* A connection to the network that is hosting the proxmox instance

### Usage
1. Clone this repository
2. Navigate to the local cloned copy
3. Copy the file path of **'main.py'**
4. Open a command prompt and run this file (python \<copied file path\>) with relevant flags and arguments:
   * -s Flag to skip SSL certificate checks **OPTIONAL**
   * -dns \<the url/hostname/IP address of target proxmox instance\> **REQUIRED**  
   * -user \<username of authorized user account\> **REQUIRED**  
   * -pwd \<password of authorized user account\> **REQUIRED**  
   * -port \<the port that will be used to connect\> **REQUIRED**  
      * 443
      * 8006
   * -ft \<the output file type \> **REQUIRED**  
      * csv
      * yaml
   * -fp \<the output file path\> **REQUIRED**  
               
  
