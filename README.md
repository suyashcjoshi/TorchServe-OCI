# TorchServe-OCI
## Serve PyTorch Models from Oracle Cloud Infrastructure(OCI) for free - 15 minutes step by step guide

1. Sign up for Oracle Cloud Always Free Service : https://www.oracle.com/cloud/free/ or login if you're already account holder 

2. Login to OCI web console : https://www.oracle.com/cloud/sign-in.html

3. Create Free Linux Instance : In order to save manual insallation steps, it's recommended to use this [pre-configured cloud developer image](https://cloudmarketplace.oracle.com/marketplace/en_US/listing/54030984) comes ready to use with popular programming languages and enviornments such as *Java, Python, Go, Node.JS and even OCI CLI and Docker etc* removing the need for manual installation. 

  * Shape : You can select any of the shapes offered but I would recommend the *Intel SkyLake CPU*
  * Leave all the default options as is and make sure to download your Private and Public key locally as you will need it for connecting to the VM from local machine.

4. Log into this free Linux instance using [SSH](https://docs.cloud.oracle.com/en-us/iaas/Content/GSG/Tasks/testingconnection.htm) from your local machine or using cloud shell from your browser. The screenshots below show login from 'cloud shell'

5. TorchServe needs JDK 11 and even if you used Developer Image it comes with JDK 8 so you need to install OpenJDK 11, which you can do by typing : `sudo apt install openjdk-11-jdk`

6. 

