from icon_cli.dapps.cps import Cps


def test_cps_get_active_proposals():
    cps = Cps("mainnet")
    proposals = cps.get_active_proposals()
    assert type(proposals) == list
    print("get_active_proposals() OK!")


def test_cps_get_progress_reports():
    cps = Cps("mainnet")
    progress_reports = cps.get_progress_reports()
    assert type(proposals) == list
    print(progress_reports)


def test_cps_get_contributors():
    cps = Cps("mainnet")
    contributors = cps.get_contributors()
    assert type(contributors) == list
    print("get_contributors() OK!")


test_cps_get_active_proposals()
test_cps_get_contributors()
test_cps_get_progress_reports()
