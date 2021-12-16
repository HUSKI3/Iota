import subprocess

def echo(*args):
  print(*args)

def execute(command):
  if "|" in command:
    # save for restoring later on
    s_in, s_out = (0, 0)
    s_in = os.dup(0)
    s_out = os.dup(1)
  
    # first command takes commandut from stdin
    fdin = os.dup(s_in)
  
    # iterate over all the commands that are piped
    for cmd in command.split("|"):
        # fdin will be stdin if it's the first iteration
        # and the readable end of the pipe if not.
        os.dup2(fdin, 0)
        os.close(fdin)
  
        # restore stdout if this is the last command
        if cmd == command.split("|")[-1]:
            fdout = os.dup(s_out)
        else:
            fdin, fdout = os.pipe()
  
        # redirect stdout to pipe
        os.dup2(fdout, 1)
        os.close(fdout)
  
        try:
            subprocess.run('bash'+cmd.strip().split())
        except Exception:
            print("SHELL: command not found: {}".format(cmd.strip()))
  
    # restore stdout and stdin
    os.dup2(s_in, 0)
    os.dup2(s_out, 1)
    os.close(s_in)
    os.close(s_out)
  else:
    try:
      if command.strip():
        subprocess.run('bash'+command.split(" "))
    except Exception as e:
      print("SHELL: {}: {}".format(e,command.strip()))