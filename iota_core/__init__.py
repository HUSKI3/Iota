from .ext import hot
import sys, getpass, os

class out:
  def __init__(self, c=None):
    self.console = c if c else sys.stdout

  def __call__(self, *args, newline=True) -> int:
    try:
      f_args = []
      for arg in args:
        f_args.append(str(arg))
      f_args = ' '.join(f_args) 
      _ = str(f_args)+'\n' if newline else str(f_args)
      self.console.write(_)
    except Exception as e:
      sys.stderr.write(f'[Failed] -- {e} \n')

class shell:

  def __init__(self, cog_path=None):
    """
    cog_path <- Location of defined cogs
    """
    self.vars           = {}
    self.pout           = out()
    self.user           = getpass.getuser()
    self._stayon        = True
    self.built_in       = self._load_built_ins(cog_path)
  
  def __call__(self) -> str:
    while self._stayon:
      try:
        self.pout(f'({self.user})> ', newline=False)
        _inp = input()
        self._process(_inp)
      except EOFError:
        self.pout(f'\n==> User closed channel, shutting console down...')
        quit()
  
  def _process(self,input) -> dict:
    inp = input.split(' ')
    if inp[0].split('.')[0] in self.built_in:
      # Found the function in a cog, let's get the function
      cog = self.built_in[inp[0].split('.')[0]]
      func = inp[0].split('.')[1]
      cog[func](' '.join(input.split(' ')[1:]))
    else:
      self.pout(f'[IOTA] Command not found')

  def _load_built_ins(self, path) -> dict:
    imp = hot.importer()
    imp.load_cogs(path) 
    builtins = {}
    for cog in imp.get_cogs():
      builtins[cog] = {}
      for x in imp.get_cogs()[cog]:
        builtins[cog][x] = imp.get_method(cog, x)
        if builtins[cog][x] is None:
          self.pout(f"<WARNING> Method {x} in {cog} has failed to load")
    return builtins

class builder:
  def __init__(self, cog_path=None, config_path=None, shell=None):
    """
    cog_path <- Location of defined cogs
    """
    self.vars           = {}
    self.pout           = out()
    self.user           = getpass.getuser()
    self.shell          = shell
    self.config         = self.get_config(config_path)

  def get_config(self, path):
    config = self.shell.built_in['yaml']['load'](path, quiet=False)
    return config

  def function(self, cog, func, *args, quiet=False):
    return self.shell.built_in[cog][func](*args, quiet=quiet)

  def script(self, script_name, project, args):
    if script_name in self.config['scripts'][project]:
      if 'env' in self.config['scripts'][project]:
        env_vars = self.config['scripts'][project]['env']
        for x in os.environ:
          env_vars[x] = os.environ[x]
        env_vars['PATH'] = env_vars['PATH'].replace('${PATH}',os.environ['PATH'])
      else:
        for x in os.environ:
          env_vars[x] = os.environ[x]
        env_vars['PATH'] = env_vars['PATH'].replace('${PATH}',os.environ['PATH'])
      for _ in self.config['scripts'][project][script_name].split('\n'):
        self.shell.built_in['shell']['execute'](_, quiet=False, vars=[env_vars])
