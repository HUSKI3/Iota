from github import Github

base_url = "https://github.com/{}/{}"

class rep:
  def __init__(self, dict) -> None:
    self.all = dict
    
  def tagged(self, tag:'tag you want the repos to match') -> list:
    x = {}
    for repo in self.all:
      if tag in self.all[repo]['tags']:
        x[repo] = self.all[repo]
    return rep(x)

def get_repos(_User:'User to get the repos from'):
  g = Github()
  user = g.get_user(_User)
  repos = {}
  for repo in user.get_repos():
    contents = repo.get_contents("")
    cnt = []
    for file in contents:
      cnt.append(file.path)
    tags = []
    [tags.append(tag) for tag in repo.get_topics()]
    repos[repo.name] = {
      'url':base_url.format(_User, repo.name),
      'content':cnt,
      'tags':tags
    }
  return rep(repos)

#get_repos('TecTone23-Mobile')