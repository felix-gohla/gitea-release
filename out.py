#!/usr/bin/env python
from giteapy.rest import ApiException
from random import randint
import giteapy
import glob
import json
import sys
import os

def main(path):
    doc = json.load(sys.stdin)

    # Configure API key authorization: AccessToken
    configuration = giteapy.Configuration()
    configuration.username = doc["source"]["owner"]
    configuration.password = doc["source"]["access_token"]
    configuration.host = doc["source"]["base_url"]

    release_id = None
    created = None
    release_url = None

    # Create a new release
    api_instance = giteapy.RepositoryApi(giteapy.ApiClient(configuration))
    owner = doc["source"]["owner"]
    repo = doc["source"]["repository"]
    body = giteapy.CreateReleaseOption(name=doc["params"]["name"], tag_name=doc["params"]["tag"], body=doc["params"]["body"])
    try:
        api_response = api_instance.repo_create_release(owner, repo, body=body)
        release_id = api_response.id
        created = api_response.created_at
        release_url = api_response.url
    except ApiException as e:
        print("Exception when calling RepositoryApi->repo_create_release: %s\n" % e, file=sys.stderr)
        sys.exit(-1)

    # Upload all given files
    files_glob = doc["params"]["files_glob"] if os.path.isabs(doc["params"]["files_glob"]) else os.path.join(path, doc["params"]["files_glob"])
    files_to_upload = glob.glob(files_glob)
    for name in files_to_upload: 
        attachment = name 
        try:
            api_response = api_instance.repo_create_release_attachment(owner, repo, release_id, attachment)
        except ApiException as e:
            print("Exception when calling RepositoryApi->repo_create_release_attachment: %s\n" % e, file=sys.stderr)
            sys.exit(-1)

    print('Created release at: {}'.format(release_url), file=sys.stderr)

    print(json.dumps({"version": {"ref": "{}".format(release_id)}, "metadata": [{"name": "uploaded_files", "value": ','.join(files_to_upload)}]}))

if __name__ == '__main__':
    main(sys.argv[1])

