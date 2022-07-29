import sys
from src import app

python_version = sys.version_info

if python_version.major < 3 or python_version.minor < 7:
    print('Recommended Python version more than 3.7.x, this python version is : %s.%s.x') % (python_version.major, python_version.minor)
elif __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) > 1:
        if arguments[1] == 'check':
            sys.exit(0)
    else:
        app.run(host="0.0.0.0", port=5000)
