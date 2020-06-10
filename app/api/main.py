import logging

from app.core import github_etl, url_haus_extraction
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
logger = logging.getLogger()


class Payload(BaseModel):
    """
    Representation of expected body structure
    Args:
        BaseModel ([type]): pydantic BaseModel, see @dataclass
    """
    repo_url: str = ''
    subfolder: str = ''
    search_keywords: list = []

    class Config:
        schema_extra = {
            'example': {
                'repo_url':
                'https://github.com/mitre/cti/',
                'subfolder':
                'enterprise-attack/attack-pattern',
                'search_keywords':
                ['type', 'spec_version', 'objects[0].x_mitre_data_sources[0]']
            }
        }


@app.post('/github-extract')
def github(payload: Payload):
    try:
        data = github_etl(payload.repo_url, payload.subfolder,
                          payload.search_keywords)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{type(e).__name__}: {e}")

    return {'data': data}


@app.get('/active-malware-urls')
def get_active_malware_urls():
    try:
        data = url_haus_extraction(
        )  # Retrieve only 1000 records to avoid swagger crash
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{type(e).__name__}: {e}")
    return {'records': len(data), 'data': data}
