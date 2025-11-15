# necessary imports (use only the python standard libraries)

# no auxiliary functions needed for this implementation

def compare_version_numbers(version1: str, version2: str) -> int:
    """
    Compares two version strings (e.g., '1.0.1' vs '1.1').

    Versions are compared numerically component by component.
    If a version runs out of components, remaining components of the
    other version are treated as zero.

    Args:
        version1: The first version string to compare.
        version2: The second version string to compare.

    Returns:
        -1 if version1 < version2
         0 if version1 == version2
         1 if version1 > version2

    Examples:
        compare_version_numbers("1.0.0", "1.0.0") == 0
        compare_version_numbers("1.0.1", "1.1") == -1
        compare_version_numbers("1.1", "1.0.1") == 1
        compare_version_numbers("1.0", "1.0.0") == 0
        compare_version_numbers("1.0.10", "1.0.2") == 1
    """
    parts1 = [int(p) for p in version1.split('.')]
    parts2 = [int(p) for p in version2.split('.')]

    max_len = max(len(parts1), len(parts2))

    for i in range(max_len):
        v1_component = parts1[i] if i < len(parts1) else 0
        v2_component = parts2[i] if i < len(parts2) else 0

        if v1_component > v2_component:
            return 1
        elif v1_component < v2_component:
            return -1
    
    return 0

# add this ad the end of the file
EXPORT_FUNCTION = compare_version_numbers
