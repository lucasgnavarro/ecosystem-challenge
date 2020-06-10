import fire
from app.core import github_etl, url_haus_extraction

if __name__ == '__main__':
    fire.Fire({
        'git_etl': github_etl,
        'url_haus_extraction': url_haus_extraction
    })
