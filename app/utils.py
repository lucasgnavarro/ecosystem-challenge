import csv
import json
import logging
import os
import re
import typing
import zipfile
from datetime import datetime

import git
import requests
from app.settings import TEMP_FOLDER

logger = logging.getLogger()


def json_decode(to_decode: str):
    try:
        decoded_json = json.loads(to_decode)
    except json.decoder.JSONDecodeError as e:
        logger.error(f'{type(e).__name__} decoding {to_decode}')
    return decoded_json


class GitHelper:
    """
    Helper class for git operations
    """
    def __init__(self, repo_url=None, branch='master'):
        if repo_url is None:
            raise ValueError('Invalid repo_url')

        self.repo_url = repo_url
        self.branch = branch
        formatted_destination_path = self.repo_url.split('://')[1].replace(
            '/', '.')
        self.destination_path = os.path.join(TEMP_FOLDER,
                                             formatted_destination_path)

    def pull(self):
        """
        Pull from github repo using provided repo_url provided on instantiation
        """
        try:
            with git.Repo(self.destination_path) as repo:
                _repo = repo.remotes.origin
                _repo.pull()
        except (git.InvalidGitRepositoryError, git.exc.NoSuchPathError) as e:
            logger.error(f'{type(e).__name__} in path {self.destination_path}')
        except Exception as e:
            logger.error(
                f"{type(e).__name__} : unhandled exception on git pull")

    def clone(self):
        """ Pull from github repo using provided repo_url provided on instantiation
        """
        try:
            _repo = git.Repo.clone_from(self.repo_url,
                                        self.destination_path,
                                        branch=self.branch)
        except git.GitCommandError as e:
            logger.error(f'{type(e).__name__} on clone repository {e}')
        except Exception:
            logger.error(
                f"{type(e).__name__} unhandled exception on git clone")

    def sync(self):
        """ git download data, if the folder exists pull else clone
        """
        if os.path.exists(self.destination_path):
            self.pull()
        else:
            os.makedirs(self.destination_path)
            self.clone()

    def extract_subfolder_data(self, subfolder: str) -> typing.Generator:
        """ given a repository subfolder, extract all the data from there and retrieve

        Args:
            subfolder (str): repository subfolder

        Returns:
            typing.Generator: generator for access to each json decoded data blob
        """
        # Update local repository
        self.sync()

        with git.Repo(self.destination_path) as repo:
            repo_chunk = repo.tree() / subfolder
            data_gen = (json_decode(blob.data_stream.read())
                        for blob in repo_chunk.blobs)

        return data_gen


class TransformationHelper:
    """
    Helper class for extraction operations
    """
    @classmethod
    def get_mapped_attributes(cls,
                              data_source: dict,
                              attrs_to_find: typing.Iterable,
                              attr_separator: str = '.') -> dict:
        """Fn to search and map the given attrs in a datasource
        Args:
            data_source (dict): data source to iterate and search given attrs to find
            attrs_to_find (typing.Iterable): list of attrs to find into data_source

        Returns:
            [dict]: dict with the mappings keys found in the given data_source
        """
        result = {}
        for attr in attrs_to_find:  # type: str
            value = cls.get_from_path(data_source, attr, attr_separator)
            if value is not None:
                result[attr] = value
        return result

    @classmethod
    def get_from_path(cls, data_source: dict, attr_path: str,
                      attr_separator: str) -> typing.Any:
        """
        Decompose the given attr_path to find the requested attr and return it
        Args:
            data_source (dict): [description]
            attr_path (str): [description]

        Returns:
            typing.Any: [description]
        """
        to_evaluate = data_source
        for attribute in attr_path.split(attr_separator):
            to_evaluate = cls.get_attribute(to_evaluate, attribute)
            if to_evaluate is None:
                return None
        return to_evaluate

    @classmethod
    def get_attribute(cls, data_source: dict, attribute: str) -> typing.Any:
        """ find the given attribute in the data_source, also checking if is a indexed attribute

        Args:
            data_source (dict): data dict to find the given attribute
            attribute (str): attribute to find in the data dict

        Returns:
            typing.Any: value if the attribute if is found else None
        """
        try:
            # Check if is an indexed attribute
            indexed_attribute = re.match(r"(\w+)\[(\d+)\]", attribute)
            if indexed_attribute:
                attribute, index = indexed_attribute.groups()
                value = data_source.get(attribute, list())[int(index)]
            else:
                value = data_source.get(attribute)
        except (AttributeError, IndexError, ValueError):
            return None
        except Exception as e:
            logger.error(
                f"{type(e).__name__} unhandled exception in get_attribute")
        return value


def to_json_file(data: typing.List[dict], destination_path: str) -> str:
    """ dump data into json file
    Args:
        data (typing.List[dict]): data to dump
        destination_path (str): path of the json file

    Returns:
        str: path of the destination json file
    """
    try:
        with open(destination_path, "w") as f:
            json.dump(data, f)
        return destination_path
    except Exception as e:
        logger.error(f"{type(e).__name__} - {e} on dump json into file")
        raise


def file_to_json(file_path: str) -> typing.Iterable:
    """load json data from file and return it

    Args:
        file_path (str): data source json file to load

    Returns:
        typing.Iterable: json structure as list, dict
    """
    try:
        with open(file_path) as output:
            data = json.load(output)
        return data
    except Exception as e:
        logger.error(f"{type(e).__name__} - {e} on dump json into file")
        raise


def get_timestamp_filename(extension: str = 'txt') -> str:
    """ Generate string for filenames with timestamp
    Args:
        extension (str, optional): file extension (json, zip, csv). Defaults to 'txt'.

    Returns:
        str: generated string, Example: 09062020_17:59:19.json
    """
    return f'{datetime.now().strftime("%d%m%Y_%H:%M:%S")}.{extension}'


def download_and_save(url: str, destination_file: str) -> str:
    """Downlad binary file from url and store in given path

    Args:
        url (str): url of the file to download
        destination_file (str): destination file to dump the content

    Returns:
        str: full destination file name
    """
    try:
        destination_folder = os.path.dirname(destination_file)

        # make the request
        req = requests.get(url)
        if req:
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            with open(destination_file, 'wb') as downloaded_file:
                downloaded_file.write(req.content)

        return destination_file

    except Exception as e:
        logger.error(
            f'{type(e).__name__} - {e} on download_and_save from {url} to {destination_file}'
        )


def extract_file(file_path: str) -> typing.Iterable:
    """Extract zip file and return the extracted list files

    Args:
        file_path (str): path of the zip file to extract

    Returns:
        [typing.Iterable]: list with all the extracted files
    """
    try:
        destination_folder = os.path.dirname(file_path)

        with zipfile.ZipFile(file_path, 'r') as zip_file:
            zip_file.extractall(destination_folder)
            extracted_files = zip_file.namelist()
        return [
            os.path.join(destination_folder, e_f) for e_f in extracted_files
        ]

    except Exception as e:
        logger.error(
            f'{type(e).__name__} - {e} on unzip_file {file_path} to {destination_folder}'
        )


def transform_csv(file_path: str):
    """Read csv from given file_path and yield dict with all the row attributes {header: row_value}

    Args:
        file_path (str): csv file path

    Yields:
        [type]: dict with all the current row attributes
    """
    headers = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if len(row) > 1:  # fast way to avoid comments in the csv file
                if line_count == 0:
                    #remove invalid characters in header
                    headers = [
                        re.sub('[^-_a-zA-Z0-9 \n\.]', '', field).strip()
                        for field in row
                    ]
                    line_count += 1
                else:
                    yield dict(zip(headers, row))
                    line_count += 1
