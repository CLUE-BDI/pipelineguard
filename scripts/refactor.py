import re

path = ".github/workflows/action.yml"
with open(path, "r") as f:
    content = f.read()

# Pattern for the "scan" job (no artifact download in between)
pattern_scan = re.compile(
    r"      - name: Setup Python 3\.12\n"
    r"        uses: actions/setup-python@v5\n"
    r"        with:\n"
    r"          python-version: 3\.12\n"
    r"\n"
    r"      - name: Install runtime dependencies\n"
    r"(?:.*?\n)+?"
    r"      - name: Set PipelineGuard environment\n"
    r"(?:.*?\n)+?"
    r"          echo \"PG_ENVIRONMENT=ci\" >> \$GITHUB_ENV\n",
    re.MULTILINE
)

# Pattern for the jobs with "Download .* artifacts" in between
pattern_with_download = re.compile(
    r"      - name: Setup Python 3\.12\n"
    r"        uses: actions/setup-python@v5\n"
    r"        with:\n"
    r"          python-version: 3\.12\n"
    r"\n"
    r"      - name: Download (.*?) artifacts\n"
    r"        uses: actions/download-artifact@v4\n"
    r"        with:\n"
    r"          name: (.*?)\n"
    r"          path: (.*?)\n"
    r"\n"
    r"      - name: Install runtime dependencies\n"
    r"(?:.*?\n)+?"
    r"      - name: Set PipelineGuard environment\n"
    r"(?:.*?\n)+?"
    r"          echo \"PG_ENVIRONMENT=ci\" >> \$GITHUB_ENV\n",
    re.MULTILINE
)

new_scan = """      - name: Setup PipelineGuard
        uses: ./.github/actions/setup-pipelineguard
        with:
          target_repo_name: ${{ inputs.target_repo_name }}
          target_repo_path: ${{ inputs.target_repo_path }}
"""

def replacement_with_download(match):
    download_name = match.group(1)
    artifact_name = match.group(2)
    path_name = match.group(3)
    return f"""      - name: Setup PipelineGuard
        uses: ./.github/actions/setup-pipelineguard
        with:
          target_repo_name: ${{{{ inputs.target_repo_name }}}}
          target_repo_path: ${{{{ inputs.target_repo_path }}}}

      - name: Download {download_name} artifacts
        uses: actions/download-artifact@v4
        with:
          name: {artifact_name}
          path: {path_name}
"""

content = pattern_scan.sub(new_scan, content, count=1)
content = pattern_with_download.sub(replacement_with_download, content)

with open(path, "w") as f:
    f.write(content)
print("Done")
