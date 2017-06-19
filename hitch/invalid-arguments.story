Invalid arguments:
  preconditions:
    files:
      key.py: |
        def invalid_method(*args, **kwargs):
            print("This method will never be run")
  scenario:
    - hitchrun:
       args: does_not_matter
       expect: key.py cannot have both
       exit_code: 1
