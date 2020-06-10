import logging
import os
import re
import typing

from app.settings import TEMP_FOLDER
from app.utils import (GitHelper, TransformationHelper, download_and_save,
                       extract_file, file_to_json, get_timestamp_filename,
                       to_json_file, transform_csv)

logger = logging.getLogger()


def github_etl(repo_url: str,
               subfolder: str,
               search_keywords: typing.Iterable[str],
               dump_file: bool = False) -> typing.Iterable:
    """Extract valuable information from github repository
    Args:
        repo_url (str): Repository base url. Example: https://github.com/mitre/cti/
        subfolder (str): The path within the repo of the datasources tha we want to use. Example: enterprise-attack/attack-pattern
        search_keywords (str): list of keys to extract from the datasources. Example ["type","spec_version",]
        dump_file (bool): if True dump transformation content into a file in temp dir with current timestamp
    Returns:
        [type]: [description]
    """
    git_repo = GitHelper(repo_url)
    subfolder_data = git_repo.extract_subfolder_data(subfolder)

    extracted_data = []
    for data in subfolder_data:
        current_data = [
            TransformationHelper.get_mapped_attributes(data, search_keywords)
            for e in data
        ]
        extracted_data += current_data

    if dump_file:
        file_name = get_timestamp_filename(extension='json')
        to_json_file(extracted_data, os.path.join(TEMP_FOLDER, file_name))
    return extracted_data


def url_haus_extraction(
    search_keywords: typing.Optional[typing.Iterable] = None):
    """Extract unique active malware urls from urlhaus
    """
    url = 'https://urlhaus.abuse.ch/downloads/csv/'
    download_path = os.path.join(TEMP_FOLDER,
                                 get_timestamp_filename(extension='zip'))

    logger.info(f'Downloading file from {url}')
    file_name = download_and_save(url, download_path)

    logger.info(f'Unzipping file {file_name}')
    extracted_files = extract_file(file_name)

    transformation_file_name = os.path.join(
        TEMP_FOLDER, get_timestamp_filename(extension='json'))
    logger.info(
        f'Making transformation to dump into {transformation_file_name}')

    if search_keywords is None:
        search_keywords = ['url']
    for path in extracted_files:
        if path.lower().endswith('.txt'):
            transformed_data = [
                TransformationHelper.get_mapped_attributes(
                    data, search_keywords) for data in transform_csv(path)
            ]

            logger.info(f'Dumping into {transformation_file_name}')
            to_json_file(transformed_data, transformation_file_name)

    # Just for didactic purposes we are loading content from file
    # We already have this data in memory
    return file_to_json(transformation_file_name)
