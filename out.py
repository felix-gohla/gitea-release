#!/usr/bin/env python
import sys
import json
import giteapy
from giteapy.rest import ApiException
from random import randint

def main(path):
    doc = json.load(sys.stdin)

    # Configure API key authorization: AccessToken
    print(doc, file=sys.stderr)
    configuration = giteapy.Configuration()
    configuration.username = doc["source"]["owner"]
    configuration.password = doc["source"]["access_token"]
    configuration.host = doc["source"]["base_url"]


    release_id = None
    created = None

    api_instance = giteapy.RepositoryApi(giteapy.ApiClient(configuration))
    owner = doc["source"]["owner"]
    repo = doc["source"]["repository"]
    body = giteapy.CreateReleaseOption(name="abc", tag_name="v0.0.1")
    try:
        # Create a release
        api_response = api_instance.repo_create_release(owner, repo, body=body)
        release_id = api_response.id
        created = api_response.created_at
    except ApiException as e:
        print("Exception when calling RepositoryApi->repo_create_release: %s\n" % e, file=sys.stderr)
        sys.exit(-1)

    attachment = '/app/out.tar.gz' # file | attachment to upload
    attachment_name = 'out.tar.gz' # str | name of the attachment (optional)

    try:
        api_response = api_instance.repo_create_release_attachment(owner, repo, release_id, attachment, name=attachment_name)
    except ApiException as e:
        print("Exception when calling RepositoryApi->repo_create_release_attachment: %s\n" % e, file=sys.stderr)
        sys.exit(-1)

    release_id = randint(1, 1337)
    json.dump({"version": {"ref": "{}".format(release_id)}, "metadata": []}, sys.stderr)
    print(json.dumps({"version": {"ref": "{}".format(release_id)}}))

if __name__ == '__main__':
    main(sys.argv[1])

