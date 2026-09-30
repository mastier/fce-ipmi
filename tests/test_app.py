import pytest

from app import Application


def test_read_machines_config_file_exists():
    application = Application(machine_config="tests/config/nodes.yaml")
    # Assert that returned dict is not empty
    assert bool(application._read_machines_config()) is True


def test_read_machines_config_file_with_list_exists():
    application = Application(machine_config="tests/config/nodes-list.yaml")
    # Assert that returned dict is not empty
    assert bool(application._read_machines_config()) is True


@pytest.mark.parametrize(
    "machine_config",
    [
        "tests/config/i-dont-exist.yaml",
        "tests/wrong-directory/nodes.yaml",
        "/root/nodes.yaml",
    ],
)
def test_read_machines_config_file_not_found(machine_config):
    application = Application(machine_config=machine_config)
    # Assert that returned dict is empty
    assert bool(application._read_machines_config()) is False


def test_read_machines_config_invalid_yaml():
    application = Application(machine_config="tests/config/nodes-invalid.yaml")
    # Assert that returned dict is empty
    assert bool(application._read_machines_config()) is False


@pytest.mark.parametrize("text", ["compute*", "compute-[12]", "node-?", "node-[!12]"])
def test_is_glob_pattern_returns_true(text):
    application = Application(machine_config="tests/config/nodes.yaml")
    assert application._is_glob_pattern(text) is True


@pytest.mark.parametrize("text", ["compute", ""])
def test_is_glob_pattern_returns_false(text):
    application = Application(machine_config="tests/config/nodes.yaml")
    assert application._is_glob_pattern(text) is False


def test_read_machines_config_hcl():
    application = Application(
        machine_config="tests/config/machines.hcl",
        bmc_passwords="tests/config/bmc_passwords",
    )
    machines = application._read_machines_config()
    assert machines["machine-01"]["bmc_user"] == "Administrator"
    assert machines["machine-01"]["bmc_address"] == "172.31.31.31"
    assert machines["machine-01"]["bmc_password"] == "hcl-secret"
    assert machines["machine-01"]["zone"] == "zone1"
    assert machines["machine-01"]["tags"] == ["ceph", "storage"]


def test_read_machines_config_hcl_env_shared(monkeypatch):
    monkeypatch.setenv("BMC_PASSWORD", "env-secret")
    application = Application(
        machine_config="tests/config/machines.hcl",
        bmc_passwords="tests/config/i-dont-exist",
    )
    machines = application._read_machines_config()
    assert machines["machine-01"]["bmc_password"] == "env-secret"


def test_read_machines_config_hcl_env_per_host(monkeypatch):
    monkeypatch.setenv("BMC_PASSWORD", '{"machine-01": "json-secret"}')
    application = Application(
        machine_config="tests/config/machines.hcl",
        bmc_passwords="tests/config/i-dont-exist",
    )
    machines = application._read_machines_config()
    assert machines["machine-01"]["bmc_password"] == "json-secret"


def test_read_machines_config_hcl_no_password(monkeypatch):
    monkeypatch.delenv("BMC_PASSWORD", raising=False)
    application = Application(
        machine_config="tests/config/machines.hcl",
        bmc_passwords="tests/config/i-dont-exist",
    )
    assert application._read_machines_config() is None


def test_read_machines_config_hcl_not_found():
    application = Application(machine_config="tests/config/i-dont-exist.hcl")
    assert bool(application._read_machines_config()) is False
