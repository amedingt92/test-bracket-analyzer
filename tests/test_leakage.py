import tempfile
import sqlite3

from src.data_cleaning import leakage_guards
from src.data_acquisition import schema


def test_leakage_guards_noop(tmp_path):
    db_path = tmp_path / "test.db"
    schema.init_db(str(db_path))
    # Should not raise
    leakage_guards.assert_no_post_asof_rows(str(db_path), 2020, "2020-03-15")
    leakage_guards.assert_feature_dates_valid(str(db_path), 2020, "2020-03-15")
