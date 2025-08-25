# How to run the tests
Run the tests with Python's unittest (from the repo root). 

Example PowerShell commands:

## Run all tests in the tests folder:

### cd to repo root first
```$PS
Set-Location 'B:\3D_Objects\GitHubClones\DGUS-Reloaded_for_CR6-Klipper_Component'
C:\Users\BadBa\AppData\Local\Programs\Python\Python313\python.exe -m unittest discover -v -s dgus_reloaded_tests -p "test_*.py"
```

## Run the single test module:

```
C:\Users\BadBa\AppData\Local\Programs\Python\Python313\python.exe -m unittest dgus_reloaded_tests.test_dwincomm
```

## Run a single test case/method:

```
C:\Users\BadBa\AppData\Local\Programs\Python\Python313\python.exe -m unittest dgus_reloaded_tests.test_dwincomm.DWINCommTests.test_init_and_config
```

### Notes

Your test already inserts the repo root onto sys.path, so imports should resolve.
If you get import errors, run from the repo root and verify the files exist at:
DWINcomm.py
test_dwincomm.py