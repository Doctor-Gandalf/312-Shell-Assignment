#!/usr/bin/python
import subprocess
import socket
import sys
import os
# TODO implement console_help.
# TODO investigate program invocation forking in case it isn't already covered (subprocess.popen()?).
# TODO add support for taking commands from file.
# Pushing to github


def change_directory(command):
    """Switch the current working directory to the directory specified.

    :param command: The command to execute, including the change_directory invocation.
    :return: True if function finished successfully, false if it was unable to complete.
    """
    if len(command) > 1:
        try:
            # TODO fix chdir adverse reaction to ~.
            # TODO investigate PWD environment variable.
            # Can't use subprocess.call here because it would only
            # change the child's directory, not the parent's.
            os.chdir(command[1])
        except OSError as e:
            print e
    else:
        print os.getcwd()
    return True


def clear():
    """Clear the terminal screen of all text.

    :return: True if function finished successfully, false if it was unable to complete.
    """
    subprocess.call(['clear'])
    return True


def directory(command):
    """Show the specified directory, or the current directory if none are specified.

    :param command: The command to execute, including the directory invocation.
    :return: True if function finished successfully, false if it was unable to complete.
    """
    command[0] = 'ls'
    subprocess.call(' '.join(command), shell=True)
    return True


def environment():
    """List the environment strings.

    :return: True if function finished successfully, false if it was unable to complete.
    """
    subprocess.call(['env'])
    return True


def echo(command):
    """Echo the user's input.

    :param command: The command to execute, including the echo invocation.
    :return: True if function finished successfully, false if it was unable to complete.
    """
    subprocess.call(command)
    return True


def console_help():
    """Show the user manual.

    :return: True if function finished successfully, false if it was unable to complete.
    """
    # TODO implement.
    return True


def pause():
    """Wait until the user hits enter again.

    :return:  True if function finished successfully, false if it was unable to complete.
    """
    raw_input('')
    return True


def default(command):
    """Execute a generic command.

    :param command: A generic command that can be run in the Unix environment.
    :return: True if function finished successfully, false if it was unable to complete.
    """
    try:
        subprocess.call(command)
    except OSError as e:
        print e
    return True


def control_commands(command):
    """Assign relevant function to execute based on a given command.

    :param command: The command to be assigned to a function.
    :return: True if shell can continue running, false if it should stop.
    """
    # Conditionals first test if it exists at all to avoid error
    # in line.index(item), thanks to the way python optimizes logical-and.
    if 'cd' in command and command.index('cd') is 0:
        return change_directory(command)
    elif 'clr' in command and command.index('clr') is 0:
        return clear()
    elif 'dir' in command and command.index('dir') is 0:
        return directory(command)
    elif 'environ' in command and command.index('environ') is 0:
        return environment()
    elif 'echo' in command and command.index('echo') is 0:
        return echo(command)
    elif 'help' in command and command.index('help') is 0:
        return console_help()
    elif 'pause' in command and command.index('pause') is 0:
        return pause()
    elif 'quit' in command and command.index('quit') is 0:
        return False
    else:
        return default(command)

if __name__ == "__main__":
    try:
        # TODO check with Prof Cardwell if he wants this to continue running after executing command line.
        # Handles command line arguments, then ends program.
        line = sys.argv[1:]
        running = control_commands(line)
    except IndexError:
        running = True
        # Continue running the shell until told to stop.
        while running:
            # Format to replicate standard Unix terminal, strictly optional but cool looking.
            info = socket.gethostname().split('.')[0] + ':' + \
                   (os.getcwd().split('/')[-1] if len(os.getcwd()) is not 1 else '/') + \
                   ' ' + os.getlogin() + '$ '

            # Can change raw_input's argument to simplify visuals.
            line = raw_input(info).split()
            running = control_commands(line)
