#!/usr/bin/env python
from giteapy.rest import ApiException
from random import randint
import giteapy
import glob
import json
import sys
import os

def absolute_path_from(maybe_absolute, absolute_prefix):
    return maybe_absolute if os.path.isabs(maybe_absolute) else os.path.join(absolute_prefix, maybe_absolute)

def main(path):
    os.chdir(path)
    doc = json.load(sys.stdin)

    # Configure API key authorization: AccessToken
    configuration = giteapy.Configuration()
    configuration.username = doc["source"]["username"]
    configuration.password = doc["source"]["access_token"]
    configuration.host = doc["source"]["base_url"]

    release_id = None
    created = None
    release_url = None

    # Create a new release
    api_instance = giteapy.RepositoryApi(giteapy.ApiClient(configuration))
    owner = doc["source"]["owner"]
    repo = doc["source"]["repository"]
    # read configuration from file
    try:
        with open(absolute_path_from(doc["params"]["tag"], path), 'r') as tag_file:
            tag_name = tag_file.read().strip()

        with open(absolute_path_from(doc["params"]["name"], path), 'r') as name_file:
            release_name = name_file.read().strip()

        with open(absolute_path_from(doc["params"]["body"], path), 'r') as body_file:
            release_body = body_file.read().strip()

    except IOError as e:
        print("Exception loading release configuration: {}".format(e), file=sys.stderr)
        sys.exit(-1)

    print("Tag Name: {}".format(tag_name), file=sys.stderr)
    print("Release name: {}".format(release_name), file=sys.stderr)
    print("Release body: {}".format(release_body), file=sys.stderr)
    release_option = giteapy.CreateReleaseOption(name=release_name, tag_name=tag_name, body=release_body)
    try:
        api_response = api_instance.repo_create_release(owner, repo, body=release_option)
        release_id = api_response.id
        created = api_response.created_at
        release_url = api_response.url
        print("Created release with id {} ({}).".format(release_id, release_url), file=sys.stderr)
    except ApiException as e:
        print("Exception when calling RepositoryApi->repo_create_release: %s\n" % e, file=sys.stderr)
        sys.exit(-1)

    # Upload all given files
    files_glob = absolute_path_from(doc["params"]["files_glob"], path)
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

