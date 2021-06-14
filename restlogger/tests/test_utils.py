from restlogger.utils import apply_hash_filter, decode_jwt_token_payload, exclude_path


def test_decode_jwt_token_payload_ok():
    jwt_token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"
        ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    )
    payload = decode_jwt_token_payload(jwt_token)
    assert payload == {"iat": 1516239022, "name": "John Doe", "sub": "1234567890"}


def test_decode_jwt_token_payload_ko():
    jwt_token = "wrong_jwt_string"
    payload = decode_jwt_token_payload(jwt_token)
    assert payload == {}


def test_exclude_path():
    path1 = "/path1/"
    path2 = "/path2/"
    assert exclude_path(path1)
    assert not exclude_path(path2)


def test_apply_hash_filter_if_path_in_settings():
    data = {
        "path": {"to": {"hash": "some value"}},
        "another": {"path": {"not to hash": "other value"}},
    }
    hashed_data = apply_hash_filter(data)
    assert hashed_data == {
        "path": {"to": {"hash": "Hash 5946210c9e93ae37891dfe96c3e39614"}},
        "another": {"path": {"not to hash": "other value"}},
    }


def test_do_not_apply_hash_filter_if_path_not_in_settings():
    data = {
        "path": {"not": {"to": {"hash": "some value"}}},
        "to": {"hash": {"not to hash": "other value"}},
    }
    hashed_data = apply_hash_filter(data)
    assert hashed_data == {
        "path": {"not": {"to": {"hash": "some value"}}},
        "to": {"hash": {"not to hash": "other value"}},
    }


def test_do_not_apply_hash_filter_if_path_is_empty():
    data = {
        "path": {"to": {"hash": ""}},
        "another": {"path": {"not to hash": "other value"}},
    }
    hashed_data = apply_hash_filter(data)
    assert hashed_data == {
        "path": {"to": {"hash": ""}},
        "another": {"path": {"not to hash": "other value"}},
    }
