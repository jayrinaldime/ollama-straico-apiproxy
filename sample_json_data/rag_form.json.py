def create_rag(
    self,
    name: str,
    description: str,
    *file_to_uploads: [Path | str],
    chunking_method: [ChunkingMethod | str] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 50,
    breakpoint_threshold_type: [
        BreakpointThresholdType | str
    ] = BreakpointThresholdType.percentile,
    buffer_size: int = 500,
) -> str:
    pass


class ChunkingMethod(Enum):
    fixed_size = "fixed_size"
    # when fixed_size display
    # chunk_size = 1000 default
    # chunk_overlap = 50 default
    recursive = "recursive"
    # when recursive display
    # chunk_size = 1000
    # chunk_overlap = 50
    markdown = "markdown"
    # when markdown display
    # chunk_size = 1000
    # chunk_overlap = 50
    python = "python"
    # when python display
    # chunk_size = 1000
    # chunk_overlap = 50
    semantic = "semantic"
    # when semantic display
    # breakpoint_threshold_type: BreakpointThresholdType = percentile
    # buffer_size = 500


class BreakpointThresholdType(Enum):
    percentile = "percentile"
    interquartile = "interquartile"
    standard_deviation = "standard_deviation"
    gradient = "gradient"
