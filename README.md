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
          - task: prepare_release
            outputs:
                - name: rel
            run: |
                echo "v0.0.1" > rel/tag.txt
                echo "Release Title" > rel/release_name.txt
                echo "Some descriptive text of this release" > rel/body.txt
          - put: release
            params:
                name: rel/release_name.txt
                tag: rel/tag.txt
                body: rel/body.txt
                files_glob: ./**/*.tgz
```
