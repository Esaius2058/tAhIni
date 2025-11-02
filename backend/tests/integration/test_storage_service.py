import io
import pytest
from src.services.storage import StorageService
from src.db.models import Uploads, User
from tests.conftest import test_db_session
from src.utils.exceptions import ServiceError

class DummySupabaseBucket:
    def __init__(self):
        self.files = {}

    def upload(self, file_name, file_obj):
        self.files[file_name] = file_obj.read()
        return True

    def download(self, file_name):
        if file_name not in self.files:
            raise FileNotFoundError("File not found")
        return self.files[file_name]

    def remove(self, names):
        for name in names:
            self.files.pop(name, None)
        return True

    def get_public_url(self, names):
        if isinstance(names, list):
            return [f"https://storage.example.com/{name}" for name in names]
        return f"https://storage.example.com/{names}"


class DummySupabaseClient:
    def __init__(self):
        self.storage = DummyStorage()

class DummyStorage:
    def from_(self, bucket_name):
        return DummySupabaseBucket()


@pytest.fixture
def storage_service(test_db_session):
    dummy_client = DummySupabaseClient()
    bucket_name = "uploads"
    return StorageService(client=dummy_client, bucket=bucket_name, db_session=test_db_session)

@pytest.fixture
def sample_user(test_db_session):
    user = User(
        name="Playboi Carti",
        email="vamp24@gmail.com",
        password="let the vamps out",
    )
    test_db_session.add(user)
    test_db_session.commit()
    yield user
    test_db_session.delete(user)
    test_db_session.commit()


@pytest.fixture
def sample_upload(storage_service, test_db_session, sample_user):
    user = test_db_session.query(User).filter(User.email == "vamp24@gmail.com").first()
    file_name = "test_upload.txt"
    user_id = user.id
    upload_obj = Uploads(filename=file_name, storage_url="https://fake.url/test_upload.txt", user_id=user_id)
    test_db_session.add(upload_obj)
    test_db_session.commit()
    yield upload_obj
    test_db_session.delete(upload_obj)
    test_db_session.commit()


def test_upload_file_success(storage_service, test_db_session, sample_user):
    file_obj = io.BytesIO(b"Sample file content")
    user = test_db_session.query(User).filter(User.email == "vamp24@gmail.com").first()

    result = storage_service.upload_file(file_obj, "myfile.txt", user.id)
    saved = test_db_session.query(Uploads).filter_by(filename="myfile.txt").first()

    assert result is not None
    assert saved is not None
    assert saved.filename == "myfile.txt"
    assert "https://storage.example.com/" in saved.storage_url


def test_upload_file_failure(monkeypatch, storage_service):
    def faulty_upload(file_name, file_obj):
        raise Exception("Upload failed")

    monkeypatch.setattr(storage_service.client.storage.from_(storage_service.bucket), "upload", faulty_upload)
    result = storage_service.upload_file(io.BytesIO(b"bad"), "fail.txt", "0488cf2b-adab-453a-88c6-d622db8656c2")

    assert result is None


def test_download_file_success(storage_service, tmp_path):
    # Prepare mock file in storage
    storage_service.client.storage.from_(storage_service.bucket).files["test.txt"] = b"Hello world"
    destination = tmp_path / "downloaded.txt"

    result_path = storage_service.download_file("test.txt", str(destination))

    assert result_path == str(destination)
    assert destination.read_bytes() == b"Hello world"


def test_download_file_not_found(storage_service, tmp_path):
    result = storage_service.download_file("missing.txt", str(tmp_path / "none.txt"))
    assert result is None


def test_delete_file_success(storage_service, sample_upload, test_db_session):
    storage_service.client.storage.from_("uploads").files[sample_upload.filename] = b"some data"
    result = storage_service.delete_file(sample_upload.filename)

    assert result is True
    assert test_db_session.query(Uploads).filter_by(filename=sample_upload.filename).first() is None


def test_delete_file_failure(monkeypatch, storage_service):
    def faulty_delete(names):
        raise Exception("Remove failed")

    monkeypatch.setattr(storage_service.client.storage.from_(storage_service.bucket), "remove", faulty_delete)
    result = storage_service.delete_file("file_that_fails.txt")

    assert result is None


def test_get_public_url_success(storage_service):
    result = storage_service.get_public_url("somefile.txt")

    assert result is not None
    assert "https://storage.example.com/somefile.txt" in result


def test_get_public_url_failure(monkeypatch, storage_service):
    def faulty_url(name):
        raise Exception("URL gen failed")

    bucket = storage_service.client.storage.from_(storage_service.bucket)
    monkeypatch.setattr(bucket, "get_public_url", faulty_url)

    with pytest.raises(ServiceError):
        storage_service.get_public_url("broken.txt")


def test_list_files(storage_service, sample_upload):
    results = storage_service.list_files()
    assert isinstance(results, list)
    assert any(upload.filename == sample_upload.filename for upload in results)


def test_list_files_by_user(storage_service, sample_upload):
    results = storage_service.list_files(user_id=sample_upload.user_id)
    assert len(results) > 0
    assert results[0].user_id == sample_upload.user_id


def test_list_files_failure(monkeypatch, storage_service):
    def faulty_query(*args, **kwargs):
        raise Exception("Query fail")

    monkeypatch.setattr(storage_service.db, "query", faulty_query)
    result = storage_service.list_files()
    assert result is None


def test_update_upload_status_success(storage_service, sample_upload, test_db_session):
    result = storage_service.update_upload_status(sample_upload.id, "processed")
    updated = test_db_session.query(Uploads).filter_by(id=sample_upload.id).first()

    assert result is True
    assert updated.status == "processed"


def test_update_upload_status_not_found(storage_service):
    result = storage_service.update_upload_status("9ee80b36-5b77-4589-a259-6a5cceff3a43", "done")
    assert result is False


def test_update_upload_status_failure(monkeypatch, storage_service):
    def faulty_commit():
        raise Exception("DB commit failed")

    monkeypatch.setattr(storage_service.db, "commit", faulty_commit)
    result = storage_service.update_upload_status("9ee80b36-5b77-4589-a259-6a5cceff3a43", "pending")

    assert result is False
