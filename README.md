# pssh

A simple tool to execute commands on multiple hosts

## Purpose

I needed to run some commands over a bunch of servers and went to my usual `dsh` but my configuration was out of date and I had a bunch of files to clean up. This is my one gripe with `dsh`, the unnecessary duplication with it's configuration files. So I had a look around and there was a Python tool called `fabric` that looked nice. But it wouldn't install

However since we are here (in Python land) and I have opinions about configuration files we would just have to write our own :)

## Usage

First we need a file that lists our hosts. Something like this, which by default we will name `machines.list` (a nod to `dsh`). The first thing on the line is the host. Either the domain name or ip address:

```
pinas.local
ubuntu.local
macm1.local
```

And then run a command, such as

```bash
$ pssh uname
```

This will run the command `uname` on all the hosts in `machines.list`

```
pinas.local : uname
pinas.local : Linux

ubuntu.local : uname
ubuntu.local : Linux

macm1.local : uname
macm1.local : Darwin
```

If the command you want to run has options, such as `uname -a`, then it would be better to place them in quotes

```bash
$ pssh "uname -a"
```

If you want to run several commands in succession then we need to write them is a file such as `test.txt`

```
uname -a
ls -l
```

and then the commands can be run with `pssh @test.txt`. Note that the file is just a list of one liners, `test.txt` is not a `bash` script. It will be executed line by line

## Groups

We can assign groups to hosts:

```
pinas.local apt
ubuntu.local apt
macm1.local brew
```

Here we are tagged the hosts according to their package manager which will allow us to run commands like. You can add as many groups as you wish on the line

```bash
$ pssh --group apt "sudo apt update"
```

If you run this you should note something. There will only be output when the command completes even if there is output as it runs so it can go quiet when it runs

Without a group all the hosts will be processed

## Information

To get a list of the hosts in the file (other than `cat` :P) you can run `pssh --list hosts` and to list the available groups `pssh --list groups`

## Configuration

By default your ssh setting for the hosts will be used but sometimes you need to configure them. There are three options `--username XXXX`, `--password XXXX` and `--port XXXX`. Just put them in `machines.list`

```
pinas.local apt --username pi --password dummy
ubuntu.local apt --username peter
macm1.local brew

```

## Finally

If `machines.list` is in the directory where the command is being executed then you do not need to specify it. However if it is elsewhere or has a different name then the `--file XXXX` option is what you are looking for
