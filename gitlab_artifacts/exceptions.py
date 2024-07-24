
# define Python user-defined exceptions
class ObjectNotFound(Exception):
    "Raised when the project is not found"
    def __init__(self, id, *args, **kwargs):
        self._type = 'object'
        if self._type.endswith('s'):
            msg = f"ERROR: {self._type} '{id}' were not found"
        else:
            msg = f"ERROR: {self._type} '{id}' was not found"
        super().__init__(msg, *args, **kwargs)

class ProjectNotFound(ObjectNotFound):
    "Raised when the project is not found"
    def __init__(self, id, *args, **kwargs):
        self._type = 'project'
        super().__init__(id=id, *args, **kwargs)

class GroupNotFound(ObjectNotFound):
    "Raised when the group is not found"
    def __init__(self, id, *args, **kwargs):
        self._type = 'group'
        super().__init__(id=id, *args, **kwargs)

class PipelineNotFound(ObjectNotFound):
    "Raised when the pipeline is not found"
    def __init__(self, id, *args, **kwargs):
        self._type = 'pipeline'
        super().__init__(id=id, *args, **kwargs)

class TagNotFound(ObjectNotFound):
    "Raised when the tag is not found"
    def __init__(self, id, *args, **kwargs):
        self._type = 'tag'
        super().__init__(id=id, *args, **kwargs)

class CommitNotFound(ObjectNotFound):
    "Raised when the commit is not found"
    def __init__(self, id, *args, **kwargs):
        self._type = 'commit'
        super().__init__(id=id, *args, **kwargs)

class PipelineJobNotFound(ObjectNotFound):
    "Raised when the job is not found"
    def __init__(self, id, *args, **kwargs):
        self._type = 'pipelines'
        super().__init__(id=id, *args, **kwargs)

class JobArtifactsNotFound(ObjectNotFound):
    "Raised when the artifacts are not found"
    def __init__(self, id, *args, **kwargs):
        self._type = 'artifacts'
        super().__init__(id=id, *args, **kwargs)
