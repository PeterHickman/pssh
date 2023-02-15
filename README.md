# pssh

A simple tool to execute commands against multiple hosts

## Purpose

I needed to run some commands over a bunch of servers and went to my usual `dsh` but my configuation was out of date and I had a bunch of files to clean up. This is my one gripe with `dsh`, the unnecessary duplication with it's configuration files. So I had a look around and there was a Python tool called `fabric` that looked nice

But it wouldn't install but since we are here (in Python land) and have opinions about configuration files we would just have to write our own

## Usage

