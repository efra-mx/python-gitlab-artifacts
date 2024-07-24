#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

"""Download artifacts from a Gitlab instance
"""

import argparse
import array
import time
import re
import json
import gitlab.exceptions
import gitlab.v4.objects
import os
import sys
from zipfile import ZipFile
import tempfile

from gitlab_artifacts.tools import *
from gitlab_artifacts.client import *
from gitlab_artifacts.finder import *


class ArtifactDownloader:
    def __init__(self, client:GitlabClient, gl_job=None, ref_name="", job_name=""):
        self.gl = client.gl
        self.project = client.project
        self.job = gl_job
        self.ref_name = ref_name
        self.job_name = job_name

    def _download_artifacts_zip(self, zip_path, **kwargs):
        # download to temporary file
        if not zip_path:
            zip_path = os.path.join(tempfile.gettempdir(), "artifacts.zip")
        zw = ZipWriter(zip_path)

        if self.job:
            # get the file from the job artifacts
            self.job.artifacts(streamed=True, action=zw)
        elif self.ref_name and self.job_name:
            # get the file from the project artifacts
            self.project.artifacts.download(streamed=True, action=zw,
                                   ref_name=self.ref_name, job=self.job_name)

        out_file_path = str(zw.output_file())
        del(zw)

        print("output file:", out_file_path)
        return out_file_path

    def download(self, zip_path='', output='', **kwargs):
        all_files = []
        zip_file = None
        zip_file = self._download_artifacts_zip(zip_path)

        if not zip_file:
            raise ValueError("Invalid job object")

        zr = ZipReader(zip_file)
        if output:
            zr.unzip(output)
            print()
            zr.list_files()
            all_files = zr.files

        if not zip_path and os.path.isfile(zip_path):
            os.remove(zip_path)
        return all_files
