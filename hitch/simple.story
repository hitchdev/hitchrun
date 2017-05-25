Run simple commands:
  preconditions:
    files:
      hitchreqs.in: |
        hitchrun
        humanize
      randommodule.py: |
        VALUE = "sometext"
      key.py: |
        from randommodule import VALUE
        import humanize
        import datetime

        def commanda():
            """
            Command A help.
            """
            print("Command A ran")

        def commandb():
            """
            Command B help.
            """
            print("Command B ran")

        def commandvar1(variable1):
            print("Command {0}".format(variable1))

        def showcwd():
            """Show current working directory."""
            print(DIR.cur)

        def showkeypath():
            """Directory where this file is located."""
            print(DIR.key)

        def showgenpath():
            """Gen directory is (~/.hitch/<< code >>/)."""
            print(DIR.gen)

        def showprojectpath():
            """Project path is path above directory containing key.py."""
            print(DIR.project)

        def humantime():
            """Use a library."""
            print(humanize.naturaltime(datetime.datetime.now()))

        def importmodule():
            print(VALUE)
  scenario:
    - hitchrun:
       args: commanda
       expect: Command A ran
    - hitchrun:
       args: commandb
       expect: Command B ran
    - hitchrun:
       args: commandvar1 C
       expect: Command C
    - hitchrun:
       args: humantime
       expect: now
    - hitchrun:
       args: showcwd
       expect: /home/vagrant
    - hitchrun:
       args: showgenpath
       expect: /home/vagrant
    - hitchrun:
       args: showkeypath
       expect: /hitchrun/state
    - hitchrun:
       args: showprojectpath
       expect: /hitchrun
    - hitchrun:
       args: importmodule
       expect: sometext
    - hitchrun:
       args: help
       expect: Command A
