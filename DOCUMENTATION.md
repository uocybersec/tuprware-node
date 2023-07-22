# Official Tuprware Node Documentation

## Table of Contents
1. [Installation](#installation)
    1. [Installing Tuprware Node on a selected node](#installing-tuprware-node-on-a-selected-node)
    2. [Setting up the proper AWS resources](#setting-up-the-proper-aws-resources)
2. [The Architecture](#the-architecture)
3. [Controlling Challenge Containers](#container-operations)
    1. [Spawning challenge containers](#spawning-challenge-containers)
    2. [Stopping challenge containers](#stopping-challenge-containers)
    3. [Restarting challenge containers](#restarting-challenge-containers)
    4. [Container port mapping](#container-port-mapping)


## Installation

### Installing Tuprware Node on a selected node

### Setting up the proper AWS resources



## The Architecture

Tuprware Node heavily relies on AWS resources. Here is a diagram outlining it's architecture: 

<img src="images/diagram.png"/>

The Tuprware Node software is installed on each Node to receive requests to spawn/stop/restart challenge containers. Tuprware Root is the interface which sends said requests to the nodes. Tuprware Root is NOT the same as Tuprware Node. 

**This repository contains the code for Tuprware Node.** 



## Container Operations

### Spawning challenge containers

### Stopping challenge containers

### Restarting challenge containers

### Container port mapping