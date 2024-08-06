#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

"""Download artifacts from a Gitlab instance
"""

import argparse
import array
import time
import re
import json
import gitlab
import gitlab.exceptions
import gitlab.v4.objects
import os
import sys
import requests
import urllib3

from gitlab_artifacts.client import *
from gitlab_artifacts.downloader import *
from gitlab_artifacts.exceptions import *


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        This script downloads artifacts from a GitLab pipeline. Most arguments
        are optional, but should not be omitted without cause.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""

        """)
    parse_add_args(parser)
    return parser.parse_args()

def parse_add_args(parser:argparse.ArgumentParser):
    parser.add_argument(
        'group',
        help='Group name')
    parser.add_argument(
        'project',
        help='Project name')
    parser.add_argument(
        '--branch', default='', dest='branch_name',
        help='Branch name')
    parser.add_argument(
        '-c', '--commit', default='',
        help='Pipeline number')
    parser.add_argument(
        '-p', '--pipeline', default=0, type=int, dest='pipeline_id',
        help='Pipeline number')
    parser.add_argument(
        '--job',
        default=os.environ.get('GITLAB_DEFAULT_JOB', default='builds'),
        dest='job_name',
        help='CI/CD job name, [env var: GITLAB_DEFAULT_JOB] or build')
    parser.add_argument(
        '--tag', default='',
        help='Repository tag')
    parser.add_argument(
        '-o', '--output', default='',
        help='output directory')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='enable verbose output')
    parser.add_argument(
        '-z', '--zip', default='', dest='zip_path',
        help='zip file')
    parser.add_argument(
        '--server',
        default=os.environ.get('GITLAB_URL', default='https://gitlab.com'),
        help='Gitlab server URL, [env var: GITLAB_URL] or https://gitlab.com')

    tokens = parser.add_mutually_exclusive_group()
    tokens.add_argument(
        "--token", dest='private_token',
        help=("GitLab private access token [env var: GITLAB_PRIVATE_TOKEN]"),
        required=False,
        default=os.getenv("GITLAB_PRIVATE_TOKEN"),
    )
    tokens.add_argument(
        "--oauth-token",
        help=("GitLab OAuth token [env var: GITLAB_OAUTH_TOKEN]"),
        required=False,
        default=os.getenv("GITLAB_OAUTH_TOKEN"),
    )
    tokens.add_argument(
        "--job-token",
        help=("GitLab CI job token [env var: CI_JOB_TOKEN]"),
        required=False,
    )
    parser.add_argument(
        '--ca-cert', default=os.environ.get('GITLAB_SSL_VERIFY', default=''),
        dest='ca_cert_file',
        help='Gitlab server SSL certificate [env var: GITLAB_SSL_VERIFY]')



def download_artifacts(server:str=None,
                       private_token:str=None,
                       ca_cert_file:str=None,
                       oauth_token:str=None,
                       job_token:str=None,
                       group='', project='',
                       branch_name='',
                       commit='', tag='', pipeline_id=0, job_name='',
                       zip_path='', output='',
                       verbose=False,
                       pristine=False,
                       **kwargs):

    if ca_cert_file:
        session = requests.Session()
        session.verify = ca_cert_file
        ssl_verify = True
    else:
        session = None
        ssl_verify = False

    client = GitlabClient(server=server,
                          private_token=private_token,
                          oauth_token=oauth_token,
                          job_token=job_token,
                          session=session,
                          ssl_verify=ssl_verify,
                          verbose=verbose)

    pipeline_job = None
    client.find_project(group=group, proj=project)

    try:
        if tag:
            # Download the artifacts from the specified pipelines
            downloader = ArtifactDownloader(client, ref_name=tag, job_name=job_name)
            downloader.download(zip_path, output, pristine=pristine)
            return

    except client.exceptions.GitlabError as e:
        # Fallback, try to get the latest commit's pipeline
        print(f"WARNING: The tag/commit {tag} does not have the artifact {job_name}")
        print("\nSearching for jobs in latest pipeline...")

    finder = PipelineJobFinder(client)
    pipeline_job = finder.find(commit, tag, pipeline_id, job_name, branch_name=branch_name)
    downloader = ArtifactDownloader(client, pipeline_job)
    downloader.download(zip_path, output, pristine=pristine)
    return pipeline_job


def main():
    import traceback

    urllib3.disable_warnings()

    args = parse_args()
    try:
        download_artifacts(**vars(args))
    except (ObjectNotFound, gitlab.exceptions.GitlabGetError) as e:
        print(e)
        print("Failed1")
        sys.exit(1)
    except Exception as e:
        print(e)
        print("Failed")
        traceback.print_exc()
        sys.exit(1)

