Run simple command without hitchreqs.in or hitchreqs.txt:
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
