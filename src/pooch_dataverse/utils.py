import pytest
from urllib.parse import urlsplit

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

def parse_url(url: str) -> ParsedURL:
    """
    Parse a URL into 3 components:

    <protocol>://<netloc>/<path>

    Example URLs:

    * http://127.0.0.1:8080/test.nc
    * ftp://127.0.0.1:8080/test.nc

    The DOI is a special case. The protocol will be "doi", the netloc will be
    the DOI, and the path is what comes after the last "/".
    The only exception are Zenodo dois: the protocol will be "doi", the netloc
    will be composed by the "prefix/suffix" and the path is what comes after
    the second "/". This allows to support special cases of Zenodo dois where
    the path contains forward slashes "/", created by the GitHub-Zenodo
    integration service.

    Parameters
    ----------
    url : str
        The URL.

    Returns
    -------
    parsed_url : dict
        Three components of a URL (e.g.,
        ``{'protocol':'http', 'netloc':'127.0.0.1:8080','path': '/test.nc'}``).

    """
    if url.startswith("doi://"):
        raise ValueError(
            f"Invalid DOI link '{url}'. You must not use '//' after 'doi:'."
        )
        
    if url.startswith("doi:"):
        protocol = "doi"
        parts = url[4:].split("/")
        if "zenodo" in parts[1].lower():
            netloc = "/".join(parts[:2])
            path = "/" + "/".join(parts[2:])
        else:
            netloc = "/".join(parts[:-1])
            path = "/" + parts[-1]
    else:
        parsed_url = urlsplit(url)
        protocol = parsed_url.scheme or "file"
        netloc = parsed_url.netloc
        path = parsed_url.path
        
    return {"protocol": protocol, "netloc": netloc, "path": path}

