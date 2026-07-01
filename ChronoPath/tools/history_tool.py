import httpx
from pydantic import BaseModel
from tenacity import retry, wait_exponential, stop_after_attempt

class HistoryResult(BaseModel):
    context: str
    facts: list[str]

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def fetch_history(place: str) -> dict:
    wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{place.replace(' ', '_')}"
    wikidata_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={place}&language=en&format=json"
    
    context = f"{place} History"
    facts = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        # Wikipedia
        try:
            w_resp = await client.get(wiki_url, headers={"User-Agent": "ChronoPath/1.0"})
            if w_resp.status_code == 200:
                data = w_resp.json()
                ext = data.get("extract")
                if ext:
                    facts.append(ext)
        except Exception:
            pass

        # Wikidata
        try:
            wd_resp = await client.get(wikidata_url, headers={"User-Agent": "ChronoPath/1.0"})
            if wd_resp.status_code == 200:
                data = wd_resp.json()
                if data.get("search"):
                    desc = data["search"][0].get("description")
                    if desc:
                        context = desc.title()
        except Exception:
            pass

    if not facts:
        facts.append("This location has regional historical relevance.")

    res = HistoryResult(context=context, facts=facts)
    return res.model_dump()
