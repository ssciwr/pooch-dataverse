import pytest

@pytest.fixture
def pooch_test_dataverse_doi():
    """
    Get a DOI for the test data stored on a DataVerse instance.

    Returns
    -------
    url
        The URL for pooch's test data.
    """
    doi = "doi:10.11588/data/TKCFEF/"
    return doi

@pytest.fixture
def pooch_test_dataverse_url():
    """
    Get the base URL for the test data stored on a DataVerse instance.

    Returns
    -------
    url
        The URL for pooch's test data.
    """
    url = "https://dataverse.org/doi:10.11588/data/TKCFEF/"
    return url