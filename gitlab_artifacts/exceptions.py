
# define Python user-defined exceptions
class ObjectNotFound(Exception):
    "Raised when the project is not found"
    _type = 'object'

    def __init__(self, id, *args, **kwargs):
        if self._type.endswith('s'):
            msg = f"ERROR: {self._type} '{id}' were not found"
        else:
            msg = f"ERROR: {self._type} '{id}' was not found"
        super().__init__(msg, *args, **kwargs)

class ProjectNotFound(ObjectNotFound):
    "Raised when the project is not found"
    _type = 'project'

    def __init__(self, id, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)

class GroupNotFound(ObjectNotFound):
    "Raised when the group is not found"
    _type = 'pipeline'
    def __init__(self, id, *args, **kwargs):
        self._type = 'group'
        super().__init__(id=id, *args, **kwargs)

class PipelineNotFound(ObjectNotFound):
    "Raised when the pipeline is not found"
    _type = 'pipeline'
    def __init__(self, id, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)

class TagNotFound(ObjectNotFound):
    "Raised when the tag is not found"
    _type = 'tag'
    def __init__(self, id, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)

class CommitNotFound(ObjectNotFound):
    "Raised when the commit is not found"
    _type = 'commit'

    def __init__(self, id, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)

class PipelineJobNotFound(ObjectNotFound):
    "Raised when the job is not found"
    _type = 'pipelines'

    def __init__(self, id, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)

class JobArtifactsNotFound(ObjectNotFound):
    "Raised when the artifacts are not found"
    def __init__(self, id, *args, **kwargs):
        self._type = 'artifacts'
        super().__init__(id=id, *args, **kwargs)
