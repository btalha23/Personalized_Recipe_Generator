## Virtual Machine EC2 SSH Setup

The first few minutes of [this video by Alexey](https://www.youtube.com/watch?v=IXSiYkP23zo) is recommended for understanding how it's done. You can then follow the below steps.

Launch a new EC2 instance. An Ubuntu OS (Ubuntu Server 24.04 LTS (HVM), SSD Volume Type, Architecture 64-bit (x86)) and a t2.large instance type, a 30Gb gp3 storage are recommended. 

**Note** - Billing will start as soon as the instance is created and run.

Create a new [key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html) so later you can connect to the new instance using SSH.

Save the .pem file in the ~/.ssh directory.

Create a config file in your `.ssh` folder

```bash
code ~/.ssh/config
```

Alternate way of creating the config file in your `.ssh` folder is

```
touch config
```

For opening the config file, you can use the command

```
nano config
```

Copy the following snippet and replace with External IP of the Virtual Machine. Username and path to the ssh private key

```bash
Host prg-llm-project
    HostName <ec2_public_ip>
    User ubuntu
    IdentityFile ~/.ssh/<key_pair_name>.pem
    StrictHostKeyChecking no
```
For saving the changes to the config file press `CTRL+O`. It will then ask you to confirm that you want to save the file. At this time, hit `ENTER`. To exit this file press `CTRL+X`.

After making these changes to `.ssh/config` file, you can SSH into the server using the command below. You can ssh into the server from different terminal windows. Just remember to change the IP address of the EC2 instance every time it restarts.

```bash
ssh prg-llm-project
```

## Virtual Machine EC2 SSH Setup

Make sure `make` and `git` are installed on the EC2 instance. If not, install them using the following command:

```bash
sudo apt update
sudo apt install -y make git
```

Clone the repository in your virtual machine.

```bash
git clone https://github.com/btalha23/Personalized_Recipe_Generator.git && \
cd Personalized_Recipe_Generator
```

Install all the tools and dependencies

```bash
make setup_ec2
```

Answer to the prompts/ questions that appear on the console window when the makefile is installing all the required tools and dependencies. A few examples where you feedback is inevitable are

![anaconda](../images/anaconda_1.png)

![anaconda](../images/anaconda_2.png)

![anaconda](../images/anaconda_3.png)