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

Stuffer design gives priority to:

* Simplicity of use. No knowledge about the tool should be required in order to use it for simple scenarios by copying
  examples. Some simplicity in the implementation is sacrificed in order to make the usage interface simple. Actions are
  named similarly to the corresponding shell commands.
* Transparency. Whenever possible, actions are translated to shell commands. All actions are logged.
* Ease of reuse. It should be simple to extract commands from snippets and convert them to reusable modules without a
  rewrite.
* Docker cache friendliness. Images built with similar commands should be able to share a prefix of commands in order to
  benefit frmo Docker image caching.
* No dislike factors. Provisioning tools tend to be loved and/or hated by users, for various reasons. There might be no
  reason to be enamoured wuth stuffer, but there should be no reason to have a strong dislike for it, given that you
  approve of Python and Docker.
* Ease of debugging. Debugging stuffer recipes should be as easy as debugging standard Python programs.

Moreover, the project model is design to facilitate sharing and reuse of code between users, see below. 

---
DSL
---






-------------------
Collaboration model
-------------------

Users are encouraged to put recipes under sites/ for others to get inspired. One package will be built for each
site. Snippets worth reuse can be put under stuffer/contrib/. Files under stuffer/contrib are expected to be maintained
by the contributor.
