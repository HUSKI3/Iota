# EZCONF
import os, subprocess, sys
import json
import re

class ezconfig:

  def __init__(self):
    self.filename = ""
    self.datajson = None

  def read(self,filename):
    """
    Reads the config file and saves the values
    :return: 
    """
    with open(str(filename),"r") as f:
      data = f.read()
      #check if the loaded file is json
      try:
        datajson = json.loads(data)
      except Exception as e:
        if True:
          print('could not load '+str(filename)+', add a basic entry to the config like {"name":"Example"}. Python error: '+str(e))
          quit()
        else:
          print("could not load "+str(filename)+". Python error: "+str(e))
          quit()
      self.datajson = datajson
      self.filename = filename
      f.close()

  def get(self,var,*args):
    """
    Return a variable
    :param var: variable to get
    :return var_val:
    """
    #update datajson
    self.read(self.filename)
    try:
      var_val = self.datajson[str(var)]
      if bool(args)!=False:
        p = re.compile('(?<!\\\\)\'')
        var_val = p.sub('\"', str(var_val))
        return json.loads(str(var_val))[str(args[0])]
    except Exception as e:
      if True:
        print("[1] could not get variable ["+str(var)+"] does it exist in config.json?\nPython error: "+str(e))
        quit()
      else:
        print(e)
    if var_val == None:
      print("[2] could not get variable ["+str(var)+"]. It equals to None, is there a python problem?")
      quit()
    else:
      return var_val
  
  def update(self,var,*args):
    """
    Update a variable
    :param var: variable to update
    """
    #update datajson
    self.read(self.filename)
    try:
      self.datajson[str(var)] = str(args[0])
    except Exception as e:
      print("could not update variable, does it exist? Did you parse a new value? Python error: "+str(e))
    jsonFile = open(str(self.filename), "w+")
    jsonFile.write(json.dumps(self.datajson))
    jsonFile.close()

  def pretty(self):
    """
    Return pretty print
    :return prettyprint:
    """
    #update datajson
    self.read(self.filename)
    try:
      return json.dumps(self.datajson, indent=4, sort_keys=True)
    except Exception as e:
      print("could not pretty print, did you load the config? Python error: "+str(e))
      quit()

  def nested(self,main,name,var):
    self.read(self.filename)
    tmp = []
    try:
      old_nested = self.get(str(main))
    except Exception as e:
      print("could not create a nested value, does the main value exist? Python error: "+str(e))
      quit()
    for elem in old_nested:
      tmp.append(elem)
    tmp.append({str(name):str(var)})
    self.datajson[str(main)] = tmp
    file = open(str(self.filename), "w")
    json.dump(self.datajson,file)
    file.close()

  def add(self,name,var):
    file = open(str(self.filename), "w")
    self.datajson[str(name)] = str(var)
    json.dump(self.datajson,file)
    file.close()

###################################################################################
class function:
  def __init__(self, function):
    self.func = function
  def __call__(self, *args, quiet=False, vars=[]):
    _out = sys.stdout
    _err = sys.stderr
    if quiet:
      sys.stdout = open(os.devnull, 'a')
      sys.stderr = open(os.devnull, 'a')
    args = list(args) + list(vars)
    ret = self.func(*args)
    if quiet:
      sys.stdout = _out
      sys.stderr = _err
    return ret

import importlib
class importer:

  def __init__(self):
    self.flags = []
    self.return_code = 0
    self.cogs = {}

  def info(self,cog_name):
    if cog_name not in self.cogs:
      quit()
    cog = self.cogs[cog_name]
    print(cog.pretty())
  
  def execute(self,cog_name,method,*args):
    if cog_name not in self.cogs:
      quit()
    cog = self.cogs[cog_name]
    m_ = importlib.import_module(cog.get('depends'))
    if method in m_.__dict__:
      f_ = function(getattr(m_, method))
      r_ = f_(*args)
      return r_
    else:
      quit()

  def get_method(self,cog_name,method,*args) -> function:
    """
    **Returns a method from a given cog**\n
    *cog_name* <- Name of the cog being accessed\n
    *method*   <- Method name\n
    *args...*
    """
    if cog_name not in self.cogs:
      quit()
    cog = self.cogs[cog_name]
    m_ = importlib.import_module(cog.get('depends'))
    if method in m_.__dict__:
      f_ = function(getattr(m_, method))
      return f_
    else:
      return None

  def get_cogs(self) -> dict:
    _ = {}
    for cog in self.cogs:
      _[cog] = self.cogs[cog].get('functions')
    return _

  def load_cogs(self,path):
    config = ezconfig()
    config.read(path)
    
    # Load each cog
    locations = config.get("locations")
    
    for cog in locations:
        cogTemp = ezconfig()
        cogTemp.read(cog)
    
        # Check output
        #print(cogTemp.pretty())
        cogName = cogTemp.get('name')
        if 'requires' in cogTemp.datajson:
          pkgs = cogTemp.datajson['requires']
          # This let's us check if dep is already installed
          reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
          installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
          for pkg in pkgs:
            print(f'<<< Checking if {pkg} is present...', end='')
            if pkg not in [i.lower() for i in installed_packages]:
              print('❌')
              subprocess.run(f"python3 -m pip install {pkg} --disable-pip-version-check".split(" "), stdout=open(os.devnull, 'wb'))
            else:
              print('✅')
        self.cogs[cogName] = cogTemp
        print(f"==> Loaded {cogName} at {cog}")