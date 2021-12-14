# IOTA - Management toolkit for TecTone 23
# Author: Artur Z  (HUSKI3 @ gh)
# Date: 10/12/2021 (Creation)

from iota_core import shell, builder
import sys

if __name__ == "__main__":
  args = sys.argv[1:]
  if args:
    _ = shell(cog_path="cogs.json")
    build = builder(config_path="android.yaml",
                    cog_path="cogs.json",
                    shell=_
                   )
    _.pout("==> Loaded in builder mode")
    build.script(args[0],args[1],args[2:])
  else:
    _ = shell(cog_path="cogs.json")
    _.pout("==> Loaded in console mode")
    _()

  