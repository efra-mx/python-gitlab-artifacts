# python-gitlab-artifacts

Tools for fetching Gitlab artifacts

It is base on python-gitlab

# Usage

```
usage: gitlab-artifacts [-h] [-c COMMIT] [-p PIPELINE] [--job JOB] [--tag TAG] [-o OUTPUT] [-v] [-z ZIP_PATH] [--server SERVER]
                        [--token PRIVATE_TOKEN | --oauth-token OAUTH_TOKEN | --job-token JOB_TOKEN] [--cert CERT_FILE]
                        group project

        This script downloads artifacts from a GitLab pipeline. Most arguments
        are optional, but should not be omitted without cause.
        

positional arguments:
  group                 Group name
  project               Project name

options:
  -h, --help            show this help message and exit
  -c COMMIT, --commit COMMIT
                        Pipeline number
  -p PIPELINE, --pipeline PIPELINE
                        Pipeline number
  --job JOB             CI/CD job name
  --tag TAG             Repository tag
  -o OUTPUT, --output OUTPUT
                        output directory
  -v, --verbose         enable verbose output
  -z ZIP_PATH, --zip ZIP_PATH
                        zip file
  --server SERVER       Gitlab server URL, [env var: GITLAB_URL] or https://gitlab.com
  --token PRIVATE_TOKEN
                        GitLab private access token [env var: GITLAB_PRIVATE_TOKEN]
  --oauth-token OAUTH_TOKEN
                        GitLab OAuth token [env var: GITLAB_OAUTH_TOKEN]
  --job-token JOB_TOKEN
                        GitLab CI job token [env var: CI_JOB_TOKEN]
  --cert CERT_FILE      Gitlab server SSL certificate [env var: GITLAB_SSL_VERIFY]  
  ```

  # Build

  ```
  pip install Build
  python -m Build
  ```

