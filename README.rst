=====================================================
Stuffer - simplified, container-friendly provisioning
=====================================================

Stuffer is a provisioning tool designed to be simple, and to be used in simple scenarios.

--------------
Project status
--------------

Just started. The documents describe intentions, most of which are not implemented.

---------
Use cases
---------

Stuffer is primarily intended to be used for provisioing container images, Docker in particular. As a secondary use
case, it can be used to provision non-production machines, e.g. developer machines.

Whereas more complex provisioning tools, such as Puppet, Chef, and Ansible, are intended for bringing a machine in any
state to a desired state, Stuffer is primarily intended for building a machine from scratch to the desired state. Since
the initial state is known, much of the complexity of existing tools is unnecessary.

--------
Overview
--------

Stuffer uses a Python embedded DSL for specifying provisioning directives. It is typically invoked with one or more
command arguments on the command line, e.g.::

  stuffer 'apt.Install("mercurial")'

Multiple arguments are concatenated into a multiple line Python recipe::

  stuffer \
    'for pkg in "mercurial", "gradle", "python-nose":' \
    '  println "Installing", pkg' \
    '  apt.Install(pkg)'

Reused recipes can be factored out into Python modules for easier reuse::

  stuffer development.Tools

  development.py:
    from stuffer.core import Group
    
    class Tools(Group):
      def children(self):
        return [apt.Install(p) for p in "mercurial", "gradle", "python-nose"]

Stuffer comes with builtin knowledge of Docker best practices, which it can enforce for you::

  Dockerfile:
    FROM phusion/baseimage:0.9.18
    ENV DEBIAN_FRONTEND noninteractive

    RUN stuffer docker.Prologue  # Verifies e.g. that base image is sound.

    RUN stuffer ... # Install stuff

    RUN stuffer docker.Epilogue  # Cleans temporary files, wanrs about known anti-patterns in the statements above.


------------
Design goals
------------

Stuffer gives priority to:

* Simplicity of use. No knowledge about the tool should be required in order to use it for simple scenarios by copying
  examples.
* Ease of reuse.
* Docker cache friendliness.
* No dislike factors.
* Ease of debugging.

In addition, the project model is design to facilitate sharing and reuse of code between users.

