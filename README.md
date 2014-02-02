Camera Alarm Setter
===================

This script is intended to enable or disable the motion triggered alarm on a
Wansview IP camera based on the availability of given hosts in the local
network.

How it works
------------

The basic workflow is like this:

               +--------------+
       +---no--+ Anyone home? +--yes----+
       |       +--------------+         |
       |                                |
       |                       +--------+----------+
       |         +---------no--+ Is it sleep time? +--yes------+
       |         |             +-------------------+           |
       |         |                                             |
       |         |                                             |
       |         |                                             |
       |         |                                 +-----------+------------+
       |         |          +-----------------yes--+ Is anyone still awake? +--no-+
       |         |          |                      +------------------------+     |
       |         |          |                                                     |
       |         |          |                                                     |
       |    +----+----------+---+                                                 |
       |    | DISABLE the Alarm |                                                 |
       |    +-------------------+                                                 |
       |                                                                          |
       |                                                                          |
       +-----------+    +---------------------------------------------------------+
                   |    |
                   |    |
            +------+----+-------+
            | ENABLE the Alarm  |
            +-------------------+

Configuration
-------------

The script is configured through a JSON file. See camalarm.json.dist for an
example. The config needs to be located right next to the Python script and be
named just like the script except for the .json extension.

``camera`` should give the IP address of your Wansview IP cam.

``user`` and ``pass`` are the access credentials you configured in your camera.

``checkminutes`` defines how often the script should go through above workflow.

To determine if anyone is at home, the script checks if any of the ``athome`` hosts
is reachable. These are usually your *mobile phones*.

Sleep times are configured by defining between which hours you usually are awake
on a given day in the ``waketime`` array.

To see if anyone is awake despite it being sleep time, the script checks if any
of the ``awake`` hosts are reachable. These are usually your *desktop computers*,
*playstation* or *TVs*.

Compatibility
-------------

This script was used with a Wansview NCB541W camera only. It might work for other
Wansview models and probably even for other Manufacturers. Pull requests welcome.
