import os 

class folder:
  def __init__(self, path, *attrs, parent = ''):
    self.path   = path
    self.attrs  = attrs
    self.parent = parent
    self.root   = os.path.dirname(os.path.realpath(__file__))
    
  def create(self):
    if 'origin' in self.attrs:
      parent = self.root.split('/cogs')[0] +'/'+ self.parent
    else:
      parent = self.root + self.parent
    path = os.path.join(parent, self.path)
    print(parent)
    try:
      os.mkdir(path)
    except FileExistsError:
      print('Path exists!')

def from_name(string:"String to be converted to a folder array", sep:'seperator',ignore:'Specify the ignore prefix', head) -> str:
  folder_struct = string.split(sep)
  # Create path
  folder_struct_formatted = '.'+'/'.join(folder_struct)
  # Check if it exists
  x = {}
  for f in os.walk('.'):
    # here we want to ignore the prefix
    if not f[0].startswith(ignore):
      x[f[0]] = f[1]
  if folder_struct_formatted in x:
    print(x[folder_struct_formatted])
  else:
    print('==> Folder not found, proceeding to create paths')
    x = []
    prev = ''
    for i in folder_struct:
      if i == head:
        folder(i,'origin').create()
      else:
        folder(i,'origin', parent=head+'/'+prev).create()
        print(f'++ Created {i}')
        prev = i

    return folder_struct_formatted[1:]