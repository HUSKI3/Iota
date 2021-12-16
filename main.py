# IOTA - Management toolkit for TecTone 23
# Author: Artur Z  (HUSKI3 @ gh)
# Date: 10/12/2021

from iota_core import shell, builder
import sys

# Config locations
config = "android.yaml"
cogs   = "cogs.json"

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

  