import re, httpx

async def github(username: str | None) -> dict:
    if not username: return {"configured": False}
    try:
        async with httpx.AsyncClient(timeout=10, headers={"Accept":"application/vnd.github+json"}) as client:
            user = (await client.get(f"https://api.github.com/users/{username}")).json()
            repos = (await client.get(f"https://api.github.com/users/{username}/repos?per_page=100")).json()
        if "message" in user: return {"configured": True, "error": "GitHub user not found"}
        languages = {}
        for r in repos:
            if r.get("language"): languages[r["language"]] = languages.get(r["language"], 0) + 1
        return {"configured": True, "username": username, "followers": user.get("followers", 0), "public_repos": len(repos), "repositories": [{"name":r["name"],"url":r["html_url"],"language":r.get("language"),"stars":r["stargazers_count"]} for r in repos[:10]], "languages": languages, "contribution_summary": "GitHub REST API exposes public repositories; contribution graph requires authenticated GraphQL access.", "bonus": min(8, len(repos) * .5)}
    except Exception as e: return {"configured": True, "error": str(e), "bonus": 0}

def validate_urls(linkedin: str | None, portfolio: str | None) -> dict:
    return {"linkedin": {"url": linkedin, "valid": bool(linkedin and re.match(r"^https?://([a-z]+\.)?linkedin\.com/", linkedin)), "notice": "OAuth integration is required for full LinkedIn profile access."}, "tableau_powerbi": {"url": portfolio, "valid": bool(portfolio and re.match(r"^https?://", portfolio) and any(x in portfolio.lower() for x in ["tableau", "powerbi", "powerbi.com"])), "bonus": 3 if portfolio and any(x in portfolio.lower() for x in ["tableau", "powerbi"]) else 0}}
