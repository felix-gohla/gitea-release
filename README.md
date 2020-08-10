# Gitea Release Concourse Resource

A resource for usage in [Concourse CI](https://concourse-ci.org) to create [Gitea](https://gitea.io/) releases and upload files.

## Usage

Here is an example pipeline config:

```yml
---
resource_types:
    - name: gitea-release
      type: registry-image
      source:
          repository: docker.io/felixgohla/gitea-release

resources:
    ...
    - name: release
      type: gitea-release
      source:
          base_url: http://gitea:3000/api/v1 # api/v1 is necessary
          owner: frank
          repository: repos_name # without .git or anything
          access_token: ((access_token)) # access token can be passed via the `--load-vars-from` fly option in `set-pipeline`

jobs:
    - name: jobname
      plan:
          - get: ...
          - task: do_smth
            ...
          - put: release
            params:
                name: Release Title
                tag: v0.0.1
                body: Some descriptive text of this release
                files_glob: ./**/*.tgz
```
