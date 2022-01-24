from github import Github

base_url = "https://github.com/{}/{}"

def get_repos(_User:'User to get the repos from'):
  g = Github()
  user = g.get_user(_User)
  repos = {}
  for repo in user.get_repos():
    contents = repo.get_contents("")
    cnt = []
    for file in contents:
      cnt.append(file.path)
    repos[repo.name] = {
      'url':base_url.format(_User, repo.name),
      'content':cnt
    }
  print(repos)