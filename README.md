README
======

This repository contains anonymised data dump from nature-quizzer project on http://www.poznavackaprirody.cz.
These data were created by system hosted at https://github.com/repli2dev/nature-quizzer repository and using
data packages hosted at https://github.com/repli2dev/nature-quizzer-packages.

Apart from original data, this repository contains parts used for basic analyses of system for the purpose of my
master thesis. The original data are in the format of backup utility bundled with the project (see its README.md).
There are also some preprocessed data for the sake of clarity of visualization preparations.

File GENERAL.md contains bunch of queries used for basic descriptional statistics.

Folder visualization contains simple python script to create visualizations using typical python libraries.

Using the data backup
=====================

Due to GitHub file limit (100 MB) the representations archive is splitted into parts.
Before using the backup join the files together with following command:
$ cat representations-* > representations.tar.gz
(SHA-1 sum is b4365349268d4ec315b61e242d303ab4cef1bbd4)
