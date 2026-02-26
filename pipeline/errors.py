class PipelineError(Exception):
    """Base class for pipeline-related errors."""
    pass


class MissingDataError(PipelineError):
    """Raised when required data is missing."""
    pass


class DisabledFeatureError(PipelineError):
    """Raised when a disabled feature is invoked."""
    pass
