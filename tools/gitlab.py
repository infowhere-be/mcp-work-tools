"""GitLab tools for mcp-work-tools."""
import os
import httpx

_GITLAB_URL = os.environ["GITLAB_API_URL"]
_GITLAB_TOKEN = os.environ["GITLAB_PERSONAL_ACCESS_TOKEN"]
_HEADERS = {"PRIVATE-TOKEN": _GITLAB_TOKEN, "Content-Type": "application/json"}


def register(mcp):
    @mcp.tool()
    def gitlab_get_issue(project_id: str, issue_iid: int) -> dict:
        """Get a GitLab issue by its IID.

        Args:
            project_id: URL-encoded project path, e.g. "sdg/r2r/right-to-repair-r2r"
            issue_iid: Issue number within the project (the number shown in the UI)
        """
        url = f"{_GITLAB_URL}/projects/{project_id}/issues/{issue_iid}"
        resp = httpx.get(url, headers=_HEADERS, verify=False)
        resp.raise_for_status()
        return resp.json()

    @mcp.tool()
    def gitlab_create_issue_note(project_id: str, issue_iid: int, body: str) -> dict:
        """Add a comment to a GitLab issue.

        Args:
            project_id: URL-encoded project path, e.g. "sdg/r2r/right-to-repair-r2r"
            issue_iid: Issue number within the project
            body: Comment text (Markdown supported)
        """
        url = f"{_GITLAB_URL}/projects/{project_id}/issues/{issue_iid}/notes"
        resp = httpx.post(url, headers=_HEADERS, json={"body": body}, verify=False)
        resp.raise_for_status()
        return resp.json()

    @mcp.tool()
    def gitlab_create_merge_request(
        project_id: str,
        title: str,
        source_branch: str,
        target_branch: str,
        description: str = "",
        draft: bool = False,
    ) -> dict:
        """Create a merge request in GitLab.

        Args:
            project_id: URL-encoded project path, e.g. "sdg/r2r/right-to-repair-r2r"
            title: MR title
            source_branch: Branch containing the changes
            target_branch: Branch to merge into (e.g. "develop")
            description: MR description (Markdown supported)
            draft: If True, creates the MR as a draft
        """
        url = f"{_GITLAB_URL}/projects/{project_id}/merge_requests"
        payload = {
            "title": f"Draft: {title}" if draft else title,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "description": description,
        }
        resp = httpx.post(url, headers=_HEADERS, json=payload, verify=False)
        resp.raise_for_status()
        return resp.json()

    @mcp.tool()
    def gitlab_list_merge_requests(
        project_id: str, state: str = "opened", per_page: int = 20
    ) -> list:
        """List merge requests in a GitLab project.

        Args:
            project_id: URL-encoded project path, e.g. "sdg/r2r/right-to-repair-r2r"
            state: Filter by state: "opened", "closed", "merged", or "all"
            per_page: Number of results to return (max 100)
        """
        url = f"{_GITLAB_URL}/projects/{project_id}/merge_requests"
        resp = httpx.get(
            url,
            headers=_HEADERS,
            params={"state": state, "per_page": per_page},
            verify=False,
        )
        resp.raise_for_status()
        return resp.json()
