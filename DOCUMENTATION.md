# Official Tuprware Node Documentation

## Table of Contents
1. [Installation](#installation)
    1. [Installing Tuprware Node on a selected node](#installing-tuprware-node-on-a-selected-node)
    2. [Setting up the proper AWS resources](#setting-up-the-proper-aws-resources)
        1. [EC2](#ec2)
        2. [Lambda](#lambda)
        3. [S3](#s3)
        4. [DynamoDB](#dynamodb)
2. [The Architecture](#the-architecture)
3. [Controlling Challenge Containers](#container-operations)
    1. [Spawning challenge containers](#spawning-challenge-containers)
    2. [Stopping challenge containers](#stopping-challenge-containers)
    3. [Restarting challenge containers](#restarting-challenge-containers)
    4. [Container port mapping](#container-port-mapping)


## Installation

### Installing Tuprware Node on a selected node
1. Once logged into your Node, clone this repository.
2. Run `./setup.sh`. Follow the intructions in the installer. 

That's it. 

### Setting up the proper AWS resources

Tuprware Node depends on the following AWS resources:

#### EC2
In Tuprware Node, an EC2 is considered a Node. You may select any instance type that fits your performance needs. 

In the EC2's security group, make sure you have the following security rules:
* Outbound Rules
    * All Traffic : `0.0.0.0/0`
* Inbound Rules
    * All TCP : `0.0.0.0/0`

Any additional security rules can be added such as restricting access to SSH (port 22), etc. 

#### Lambda

In Tuprware Node, we use a Lambda function to query the DynamoDB.

When creating your Lambda, make sure the runtime is set to `Python 3.10`.

Additionally, the role which you created/reused for the Lambda, must have the following permissions:
* `AmazonDynamoDBFullAccess`

To upload the code to your Lambda do the following:
1. Download the code from the [`dynamodb_lambda`](https://github.com/uocybersec/tuprware-node/tree/dynamodb_lambda) branch. 
2. 




#### S3



#### DynamoDB


For the future, we could use the [Serverless framework](https://www.serverless.com/) to programmatically generate and configure the AWS resources for Tuprware Node.


## The Architecture

Tuprware Node heavily relies on AWS resources. Here is a diagram outlining it's architecture: 

<img src="images/diagram.png"/>

### Important notes

Turpware Node can be installed on as many Nodes as desired. In this diagram, I chose 3 Nodes. 

The Tuprware Node software is installed on each Node to receive requests to spawn/stop/restart challenge containers. Tuprware Root is the interface which sends said requests to the nodes. Tuprware Root is NOT the same as Tuprware Node. 

**This repository contains the code for Tuprware Node.** 



## Container Operations

### Spawning challenge containers

### Stopping challenge containers

### Restarting challenge containers

### Container port mapping