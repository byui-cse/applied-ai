# Role

You are a cloud engineer, who is skilled at optimizing for cost, requirements, and perfection. 

# Task

Your **task** is to create an ubuntu EC2 so that I can clone the canvas LMS into the EC2 so I can edit the files there without crowding up my local machine. The AWS cli is already authenticated and setup. All will go inside of the us-east-1 region.

# Steps

Complete the following steps in order

1. Make sure aws cli is installed
2. Create an Ubuntu EC2. This needs to be big enough and with enough memory to be able to clone Canvas LMS and to run basic commands.
3. Download the pem file and place it into this directory
4. Perform a chmod 400 to the pem file
5. Append a SSH configuration for this instance in the ~/.ssh/config file.
6. Clone the https://github.com/chaseWillden/canvas-lms repository successfully into the EC2.

```
Host canvas-lms
    HostName <ip of the ec2>
    IdentityFile <path to pem>
    User ubuntu
```