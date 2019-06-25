# File called _pytest for PyCharm compatability
import pytest

from eland.tests import *

from pandas.util.testing import (
    assert_almost_equal, assert_frame_equal, assert_series_equal)

import eland as ed

class TestMapping():

    # Requires 'setup_tests.py' to be run prior to this
    def test_mapping(self):
        mappings = ed.Mappings(ed.Client(ELASTICSEARCH_HOST), TEST_MAPPING1_INDEX_NAME)

        assert mappings.all_fields() == TEST_MAPPING1_EXPECTED_DF.index.tolist()

        assert_frame_equal(TEST_MAPPING1_EXPECTED_DF, pd.DataFrame(mappings.mappings_capabilities['es_dtype']))

        assert mappings.count_source_fields() == TEST_MAPPING1_EXPECTED_SOURCE_FIELD_COUNT

    def test_copy(self):
        mappings = ed.Mappings(ed.Client(ELASTICSEARCH_HOST), TEST_MAPPING1_INDEX_NAME)

        assert mappings.all_fields() == TEST_MAPPING1_EXPECTED_DF.index.tolist()
        assert_frame_equal(TEST_MAPPING1_EXPECTED_DF, pd.DataFrame(mappings.mappings_capabilities['es_dtype']))
        assert mappings.count_source_fields() == TEST_MAPPING1_EXPECTED_SOURCE_FIELD_COUNT

        # Pick 1 source field
        columns = ['dest_location']
        mappings_copy1 = ed.Mappings(mappings=mappings, columns=columns)

        assert mappings_copy1.all_fields() == columns
        assert mappings_copy1.count_source_fields() == len(columns)

        # Pick 3 source fields (out of order)
        columns = ['dest_location', 'city', 'user_name']
        mappings_copy2 = ed.Mappings(mappings=mappings, columns=columns)

        assert mappings_copy2.all_fields() == columns
        assert mappings_copy2.count_source_fields() == len(columns)

        # Check original is still ok
        assert mappings.all_fields() == TEST_MAPPING1_EXPECTED_DF.index.tolist()
        assert_frame_equal(TEST_MAPPING1_EXPECTED_DF, pd.DataFrame(mappings.mappings_capabilities['es_dtype']))
        assert mappings.count_source_fields() == TEST_MAPPING1_EXPECTED_SOURCE_FIELD_COUNT