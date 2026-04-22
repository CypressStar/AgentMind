FAILURE_KINDS = [
    "runtime_error",
    "test_failure",
    "api_failure",
    "tool_failure",
    "quality_failure",
    "reasoning_failure",
]

FAILURE_SIGNAL_SOURCES = [
    "system_or_runtime",
    "test_or_validation",
    "api_response",
    "tool_execution",
    "user_feedback",
]

WORK_DOMAINS = [
    "api-integration",
    "tool-usage",
    "code-implementation",
    "test-and-verification",
    "frontend-ui",
    "repo-and-filesystem",
    "research-and-analysis",
    "docs-and-content",
]

REF_TYPES = [
    "official_doc",
    "api_error",
    "tool_limit",
    "user_constraint",
    "test_result",
]

FEEDBACK_HINTS = [
    "not_resolved",
    "wrong_direction",
    "misunderstood_request",
    "too_generic",
    "low_quality",
    "format_or_output_mismatch",
]

ATTEMPT_RESULTS = [
    "failed",
    "passed",
    "signal",
]
