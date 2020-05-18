====================
BrowseContent
====================
Author: HanishKVC
Version: v20200515IST1022


General
==========

Allow one to browse through file directories and view content files like Videos,
PDFs, Html, etc within the application.

It maintains info as to which was the last file viewed/played in that session
and inturn the same is saved into a hidden file at the base directory passed
to the program when it was started. So if next time the user passes the same
base directory path to the program, then it will automatically cd into the
last viewed files directory and highlight the last played file.


Dependencies
================

This uses

* Python3

* GTK3

* Webkit2 library

  * GStreamer and its plugins

* Evince library

The above is based on its default configuration.

If one configures the code to use external viewers, then one requires to install
the needed programs, as will be triggered by xdg-open, if one were to ask it to
play/view/open a given content.


TODO
========

Have to pick the list of extensions to skip from file/dir listing shown by prg,
from a config file


Urge for creating / Scratch the Itch
======================================

I had a need to go through sequenced course contents which I had on my machine,
in a structured manner when required. So created this program.

By sequenced what I mean is that the sub directories and files within them are
numbered/named so that if one sorts the contents based on their name, it is in
the required sequence in which one needs to go through them.

