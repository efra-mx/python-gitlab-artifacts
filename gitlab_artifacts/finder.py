#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

"""Download artifacts from a Gitlab instance
"""

import gitlab
import gitlab.exceptions
import gitlab.v4.objects
from gitlab.v4.objects import *
from .exceptions import *
from .client import *



class PipelineJobFinder:
    def __init__(self, client:GitlabClient):
        self.gl = client.gl
        self.project = client.project
        self.project.lazy = True

    def get_job_names(self, pipeline):
        jobs = pipeline.jobs.list()
        jobs = [ j.name for j in jobs ]

        return jobs

    def _find_job(self, pipeline, job_name):
        if not job_name:
            return None

        proj = self.gl.projects.get(pipeline.project_id)
        job = None
        jobs = pipeline.jobs.list()
        for j in jobs:
            if j.name == job_name and j.status == 'success':
                job = proj.jobs.get(j.id)
                break
        return job

    def find_commit(self, commit_id=None, tag=None, pipeline_id=0):
        _tag = None
        commit = None
        mode = "Commit"

        try:
            if commit_id:
                commit = self.project.commits.get(commit_id)
            elif tag and not commit:
                mode = "Tag"
                _tag = self.project.tags.get(tag)
                commit = self.project.commits.get(_tag.commit['id'])
            elif pipeline_id:
                mode = "Pipeline"
                pipeline = self.project.pipelines.get(pipeline_id)
                commit = self.project.commits.get(pipeline.sha)
        except gitlab.exceptions.GitlabGetError as e:
            if e.response_code != 404:
                return None
            if mode == "Commit":
                raise CommitNotFound(commit)
            if mode == "Tag":
                raise TagNotFound(tag)
            if mode == "Pipeline":
                raise PipelineNotFound(pipeline)

        return commit


    def find_commit_pipeline(self, commit, pipeline_id=0):
        # find the latest pipeline if not specified
        if (not pipeline_id) and commit:
            pipeline_id = commit.last_pipeline['id']
        
        if not pipeline_id:
            raise FileNotFoundError("No valid pipeline found")
        pipeline = self.project.pipelines.get(pipeline_id)

        return pipeline

    # Find the job instance
    def find(self, commit='', tag='', pipeline_id=0, job_name=''):
        commit_obj = self.find_commit(commit, tag, pipeline_id)
        pipeline = self.find_commit_pipeline(commit_obj, pipeline_id)
        print(f"tag: {tag}")
        print(f"commit: {commit_obj.short_id}: {commit_obj.title}")
        print(f"pipeline.id: {pipeline.id}")
        job = self._find_job(pipeline, job_name)
        if job:
            print(f"job.id: {job.id}")
            print(f"job.name: {job.name}")
            if not job.artifacts:
                raise JobArtifactsNotFound(job.name)
        else:
            print("Available jobs:")
            [ print('\t', j.name) for j in pipeline.jobs.list() if j.status == 'success' ]
            print("Jobs with no artifacts:")
            [ print('\t', j.name) for j in pipeline.jobs.list() if not j.artifacts ]
            print("Manual jobs:")
            [ print('\t', j.name) for j in pipeline.jobs.list() if j.status == 'manual' ]
            raise PipelineJobNotFound(job_name)
        return job

