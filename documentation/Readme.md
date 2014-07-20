An attempt to get a starting point for a community built something like IDA.

I have already replicated the interface, built a plugin system, and made a simple example.
I got it as far as any reasonable human working alone can be expected to...
Now it just needs community sponsors and team builds of plugins.

I mean, I am human.  I do need a team.

The source is mostly self-documenting, but the general concepts are outlined here.  For installation
skip right to the end.

Design goals:
Should be able to be run headless.
User interface should be decoupled from the work bits.

Installation:
It's built to run in a venv with system-site-packages enabled for the pygi parts.
If someone wants to work on building pygi inside a venv, I am quite sure myself among others would appreciate it.

Dependencies:
Pygi.
My tweaked distorm3 wrapper to work with py3k.
#Hopefully to be replaced, but it works to get it to the starting line
My tweaked gtkpyconsole to work with py3k.
My hexed widget for pygi.
My tweaked xdot to work with py3k.
python3-magic for the fileid plug-in.
