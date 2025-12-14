import pooch_dataverse


def test_pooch_dataverse():
    assert pooch_dataverse.add_one(1) == 2
