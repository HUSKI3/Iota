# IOTA - Management toolkit for TecTone 23
# Author: Artur Z  (HUSKI3 @ gh)
# Date: 10/12/2021

from iota_core import shell, builder
import sys

# Config locations
config = "android.yaml"
cogs   = "cogs.json"

# Here we can modify the builder to our heart's content
class AndroidBuilder(builder):
  
  def __init__(self, config_path, cog_path, shell) -> None:
    # Init Shell
    self.shell = shell
    # Init our builder
    builder.__init__(self,
      config_path=config_path,
      cog_path=cogs,
      shell=self.shell
    )

    def print(*args):
      self.shell.pout(*args)

    # Process our config
    # Use proc_load to process our custom yaml syntax first into pre
    pre = self.function('yaml','proc_load',config, self.config)
      
    # Prep for build
    self.repos = self.function('repo','get_repos','TecTone23-Mobile')
    self.tobuild = self.repos.tagged('autobuild')
    
    # Now we have a dictionary of repos that we need to build
    for repo in self.tobuild:
      #print(repo, self.tobuild[repo])

      # Let's convert them to a folder structure using the folders cog
      path = self.function('folders','from_name',
                    repo,     # Folder to create
                    '_',      # Seperator
                    './.',    # Ignore this case
                    'platform' 
                   )
      self.tobuild[repo].clone(path)

  def run(self):    
    self.script('test','mono',None)

_ = shell(cog_path=cogs)
builder = AndroidBuilder(config, cogs, _)

if __name__ == "__main__":
  args = sys.argv[1:]
  if args:
    builder.run()
  else:
    _.pout("==> Loaded in console mode")
    _()