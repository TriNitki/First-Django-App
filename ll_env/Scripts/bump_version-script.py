#!C:\Users\Danil\Desktop\gitik\learning\ll_env\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pyproject==1.3.1','console_scripts','bump_version'
__requires__ = 'pyproject==1.3.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pyproject==1.3.1', 'console_scripts', 'bump_version')()
    )
