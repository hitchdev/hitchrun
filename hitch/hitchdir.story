Run commands in a directory called hitch:
  description: |
    In a project folder.
  preconditions:
    linkfile: hitch
    files:
      hitch/key.py: |
        def commanda():
            """
            Command A help.
            """
            print("Command A ran")
  scenario:
    - hitchrun:
       args: commanda
       expect: Command A ran
