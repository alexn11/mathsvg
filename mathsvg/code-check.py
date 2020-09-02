import subprocess

# old version
# subprocess.call([ "flake8", "--ignore=W391,E111,E114,E201,E202,E203,E211,E251,E261,E265,E266,E303,E501,W291,W293", "mathsvg.py"] )
subprocess.call([ "flake8", "--ignore=E111,E114,E201,E202,E251,E265,E303,W391,E501", "mathsvg.py"] )

