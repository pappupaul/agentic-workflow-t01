#!/usr/bin/env python3
"""
Demo pipeline: run linter (flake8) and tests (pytest).
"""
import subprocess
import sys


def run(cmd):
    print('\n$ ' + ' '.join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print('Command not found:', cmd[0])
    except subprocess.CalledProcessError as e:
        print('Command failed with exit code', e.returncode)


def main():
    print('Demo: Auto lint and test pipeline')
    print('Step 1: Linting with flake8')
    run([sys.executable, '-m', 'flake8', '.'])

    print('\nStep 2: Running tests with pytest')
    run([sys.executable, '-m', 'pytest', '-q'])


if __name__ == '__main__':
    main()
