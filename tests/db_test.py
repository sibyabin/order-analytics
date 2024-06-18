from order_analytics.core.commons.db import DbManager
from order_analytics.core.commons.logger import Logger

log = Logger("tests")
dbmgr = DbManager(log)


def test_select():
    """ """
    assert dbmgr.select("SELECT 1 UNION ALL SELECT 2") == [(1,), (2,)]


def test_select_one():
    """ """
    assert dbmgr.select_one("SELECT 1 UNION ALL SELECT 2") == (1,)
