import json
from pathlib import Path


def test_public_fixture_is_artificial_only():
    data = json.loads(Path('data/fixtures/public_fixture.json').read_text(encoding='utf-8'))
    assert data['artificialDataOnly'] is True
    assert data['sourceGameDataIncluded'] is False
    for profile in data['profiles']:
        assert profile['profileId'].endswith('_TEST')
        for asset in profile['assets']:
            assert asset['className'].startswith('A3CDB_Test_')
            assert asset['configRoot'].startswith('Cfg')


def test_no_real_profile_names():
    text = Path('data/fixtures/public_fixture.json').read_text(encoding='utf-8')
    for forbidden in ('TOTAL_V2', 'V008', 'P0_REAL', 'P5_REAL'):
        assert forbidden not in text
