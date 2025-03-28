#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

"""Download artifacts from a Gitlab instance
"""

import gitlab
import gitlab.exceptions
import gitlab.v4.objects
from .exceptions import *


class GitlabClient:
    def __init__(self,
                 gl:gitlab.Gitlab=None,
                 group:str=None,
                 proj:str=None,
                 server:str=None,
                 private_token:str=None,
                 oauth_token:str=None,
                 job_token:str=None,
                 session=None,
                 ssl_verify:bool=False,
                 verbose=False
                 ):
        self.private_token = private_token
        self.oauth_token = oauth_token
        self.job_token = job_token
        self.project = None
        if not gl:
            gl = gitlab.Gitlab(server, private_token, session=session,
                               ssl_verify=ssl_verify)
        self.gl = gl
        if verbose:
            gl.enable_debug()
        if group and proj:
            self.project = self.find_project(group, proj)

    def find_project(self, group, proj, per_page=50):
        # Find the groups
        groups = self.gl.groups.list(search=group, per_page=50)
        _group = None
        for item in groups:
            if item.name.lower() == group.lower():
                _group = item
                break

        if not _group:
            raise GroupNotFound(group)

        # Find the project
        projects = _group.projects.list(search=proj)
        _project = None
        for item in projects:
            print(item.name, item.id)
            if item.name.lower() == proj.lower():
                _project = self.gl.projects.get(item.id)
                break

        if not _project:
            raise ProjectNotFound(proj)
        self.project = _project

    def get_tags(self):
        tag_objs = self.project.tags.list(all=True)
        tags = [ tag.name for tag in tag_objs ]

        return tags
