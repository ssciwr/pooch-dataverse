class DataverseRepository(DataRepository):  # pylint: disable=missing-class-docstring
    def __init__(self, doi, archive_url):
        self.archive_url = archive_url
        self.doi = doi
        self._api_response = None

    @classmethod
    def initialize(cls, doi, archive_url):
        """
        Initialize the data repository if the given URL points to a
        corresponding repository.

        Initializes a data repository object. This is done as part of
        a chain of responsibility. If the class cannot handle the given
        repository URL, it returns `None`. Otherwise a `DataRepository`
        instance is returned.

        Parameters
        ----------
        doi : str
            The DOI that identifies the repository
        archive_url : str
            The resolved URL for the DOI
        """
        # Access the DOI as if this was a DataVerse instance
        response = cls._get_api_response(doi, archive_url)

        # If we failed, this is probably not a DataVerse instance
        if 400 <= response.status_code < 600:
            return None

        # Initialize the repository and overwrite the api response
        repository = cls(doi, archive_url)
        repository.api_response = response
        return repository

    @classmethod
    def _get_api_response(cls, doi, archive_url):
        """
        Perform the actual API request

        This has been separated into a separate ``classmethod``, as it can be
        used prior and after the initialization.
        """
        # Lazy import requests to speed up import time
        import requests  # pylint: disable=C0415

        parsed = parse_url(archive_url)
        response = requests.get(
            f"{parsed['protocol']}://{parsed['netloc']}/api/datasets/"
            f":persistentId?persistentId=doi:{doi}",
            timeout=DEFAULT_TIMEOUT,
        )
        return response

    @property
    def api_response(self):
        """Cached API response from a DataVerse instance"""

        if self._api_response is None:
            self._api_response = self._get_api_response(
                self.doi, self.archive_url
            )  # pragma: no cover

        return self._api_response

    @api_response.setter
    def api_response(self, response):
        """Update the cached API response"""

        self._api_response = response

    def download_url(self, file_name):
        """
        Use the repository API to get the download URL for a file given
        the archive URL.

        Parameters
        ----------
        file_name : str
            The name of the file in the archive that will be downloaded.

        Returns
        -------
        download_url : str
            The HTTP URL that can be used to download the file.
        """
        parsed = parse_url(self.archive_url)
        response = self.api_response.json()
        files = {
            file["dataFile"]["filename"]: file["dataFile"]
            for file in response["data"]["latestVersion"]["files"]
        }
        if file_name not in files:
            raise ValueError(
                f"File '{file_name}' not found in data archive "
                f"{self.archive_url} (doi:{self.doi})."
            )
        # Generate download_url using the file id
        download_url = (
            f"{parsed['protocol']}://{parsed['netloc']}/api/access/datafile/"
            f"{files[file_name]['id']}"
        )
        return download_url

    def populate_registry(self, pooch):
        """
        Populate the registry using the data repository's API

        Parameters
        ----------
        pooch : Pooch
            The pooch instance that the registry will be added to.
        """

        for filedata in self.api_response.json()["data"]["latestVersion"]["files"]:
            pooch.registry[filedata["dataFile"]["filename"]] = (
                f"md5:{filedata['dataFile']['md5']}"
            )