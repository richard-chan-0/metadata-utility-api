import src.services as Services
from src.data_types import ServiceMetaData
from src.exceptions.exceptions import InvalidService
from pytest import raises


class TestServices:
    def test_return_service_returns_a_service_class_obj(self):
        service_name = Services.ORGANIZE_CHAPTERS_TO_VOL_NAME
        service = Services.return_service(service_name)

        assert service is not None

    def test_return_service_throws_exception_with_invalid_service_name(self):
        bad_service_name = "bad service name"
        with raises(InvalidService):
            Services.return_service(bad_service_name)
