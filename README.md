![Iota](logo-iota.png)
# Iota
> A quick and easy monolith project management utility

Iota provides a simple to use interface, you can either use the Console or the Builder modes. A Console is an interactive CLI utility which let's you call functions from your cogs or even build in there, while the builder is a single command which automates the building/testing/deployment processes.

### Console
Using the console is simple (example output):
```bash
$ iota
==> Loaded hello at cogs/example_cog/package.json
==> Loaded in console mode
(Huski3)> 
```
Here you can call any of the cogs that you have loaded. A cog is a library which can be attached to a project and used across any of it's children. This is an example cog structure:
> folder structure

```
|- cogs
    \_ example_cog
        \_ hello.py
        \_ package.json
```
> package.json structure

```json
{
  "name":"hello",
  "version":"0.0.1",
  "functions":[ 
    "hello", // Functions defined in the python file
    "world"
  ],
  "variables":"multi",
  "depends":"cogs.hello"  // Name of the python file here ,
  "requires":["example"] // Pip packages can be specified here
}
```
Now that we have our cog defined, this is how you define a project:
> project.yaml

```yml
project: &project
  name: "Example Monolith"
  type: "monolith"
  maintainer:
    name: "Your Name"
    email: "Your Email"
  children: [
              "child"
            ]
  depends: [
              "cogs/example_cog"
           ]

scripts:
  mono:
    prep: |
      echo ==> Doing something here 
    build: |
      echo ==> Building something here
    test: |
      tests/run-all-tests.sh

  child:
    build: |
      echo ==> Doing something here too
    test: |
      cat kernel/tests.txt
```
Once you have that we need to specify our cogs location for HotImport to load:
> cogs.json

```json
{
	"name":"Example Cogs",
	"version":"0.0.1",
	"locations":[
    "cogs/example_cog/package.json"
  ],
	"status":"rolling"
}
```
