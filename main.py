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
  
  def __init__(self, config, cogs, shell) -> None:
    self.repos = get_repos('TecTone23-Mobile')
    # Init Shell
    shell = shell(cog_path=cogs)
    # Init our builder
    builder.__init__(
      config_path=config,
      cog_path=cogs,
      shell=shell
    )
    # Now run the actual scripts
    self.script('test','mono',None)


if __name__ == "__main__":
  args = sys.argv[1:]
  _ = shell(cog_path=cogs)
  if args:
    build = builder(config_path=config,
                    cog_path=cogs,
                    shell=_
                   )
    _.pout("==> Loaded in builder mode")
    build.script(args[0],args[1],args[2:])
  else:
    _.pout("==> Loaded in console mode")
    _()  