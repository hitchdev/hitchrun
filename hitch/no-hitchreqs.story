Non-existent hitchreqs.in and hitchreqs.txt:
  description: |
    If hitchreqs.in and hitchreqs.txt both do not
    exist then one, then the other are both created
    on the fly.
  preconditions:
    files:
      key.py: |
        def commanda():
            """
            Command A help.
            """
            print("Command A ran")
  scenario:
    - hitchrun:
       args: commanda
       expect: Command A ran
