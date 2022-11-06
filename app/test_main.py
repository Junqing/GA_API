from fastapi.testclient import TestClient
import random
import math
from .main import app

client = TestClient(app)

fibonacci_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]


def test_fibonacci_index():
    """
    Testing for fetching with positive integers of the first 11 positions
    of the fibonacci sequence
    """
    for n in range(20):
        test_input = random.randint(0, 10)
        response = client.get(f"/fibonacci/{test_input}")
        assert response.status_code == 200
        assert response.json()["value"] == fibonacci_sequence[test_input]


def test_fibonacci_index_error():
    """
    Test the fibonacci index fetch for invalid input:
    - negative input
    - string input
    - float input
    - non input
    - large input
        (the output fibonacci number becomes too big for int type to handle)
    """
    negative_input = -5
    response = client.get(f"/fibonacci/{negative_input}")
    assert response.status_code == 422
    invalid_input = "test"
    response = client.get(f"/fibonacci/{invalid_input}")
    assert response.status_code == 422
    non_input = None
    response = client.get(f"/fibonacci/{non_input}")
    assert response.status_code == 422
    float_input = 12.3
    response = client.get(f"/fibonacci/{float_input}")
    assert response.status_code == 422
    large_input = 50000
    response = client.get(f"/fibonacci/{large_input}")
    assert response.status_code == 422


def test_fibonacci_sequence():
    """
    Test fetching a sequence of fibonacci
    where the requested length is smaller than max page size
    Test paginating with incremental pages and output
    """
    input = 11
    page = 1
    size = 100
    response = client.get(
        f"/fibonacci/sequence/{input}?page={page}&size={size}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["page"] == page
    assert response_data["size"] == size
    assert [item["value"]
            for item in response_data["items"]] == fibonacci_sequence


def test_fibonacci_sequence_pagination():
    """
    Test fetching the sequence of fibonacci
    where the requested length is bigger than max page size
    triggering the pagination
    """
    input = 150
    size = 100
    total_pages = math.ceil(input/size)
    for page_number in range(1, total_pages+1):
        response = client.get(
            f"/fibonacci/sequence/{input}?page={page_number}&size={size}")
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["page"] == page_number
        response_fibonacci_sequence = response_data["items"]
        if page_number < total_pages:
            assert len(response_fibonacci_sequence) == size
        else:
            assert len(response_fibonacci_sequence) == input % size


def test_fibonacci_sequence_pagination_error():
    """
    Test the fibonacci index fetch for invalid input:
    - negative input
    - string input
    - float input
    - non input
    """
    negative_input = -5
    response = client.get(f"/fibonacci/sequence/{negative_input}")
    assert response.status_code == 422
    invalid_input = "test"
    response = client.get(f"/fibonacci/sequence/{invalid_input}")
    assert response.status_code == 422
    non_input = None
    response = client.get(f"/fibonacci/sequence/{non_input}")
    assert response.status_code == 422
    float_input = 12.3
    response = client.get(f"/fibonacci/sequence/{float_input}")
    assert response.status_code == 422


def test_create_undo_blacklist():
    """
    Test 
    - fetching a valid fibonacci number,
    - blacklisting it
    - fetch with expected errors
    - undo the blacklist
    - fetch the valid fibonacci number again
    """
    input = 5
    fibonacci_index = fibonacci_sequence.index(input)
    # First test fetching the value from fibonacci
    fibonacci_response = client.get(f"/fibonacci/{input}")
    assert fibonacci_response.status_code == 200
    fibonacci_sequence_response = client.get(
        f"fibonacci/sequence/{fibonacci_index+1}")
    assert fibonacci_sequence_response.status_code == 200
    assert input in [item["value"]
                     for item in fibonacci_sequence_response.json()["items"]]

    # Now blacklisting this input
    blacklist_response = client.post(f"/fibonacci/blacklist/{input}")
    assert blacklist_response.status_code == 201

    # The number should not be in the previously successful fetch output
    fibonacci_response = client.get(f"/fibonacci/{input}")
    assert fibonacci_response.status_code == 422
    fibonacci_sequence_response = client.get(
        f"fibonacci/sequence/{fibonacci_index+1}")
    assert fibonacci_sequence_response.status_code == 200
    assert input not in [item["value"]
                         for item
                         in fibonacci_sequence_response.json()["items"]]

    # Now undo the blacklisted value
    undo_blacklist_response = client.delete(
        f"fibonacci/blacklist/undo/{input}")
    assert undo_blacklist_response.status_code == 204
    fibonacci_response = client.get(f"/fibonacci/{input}")
    assert fibonacci_response.status_code == 200
    fibonacci_sequence_response = client.get(
        f"fibonacci/sequence/{fibonacci_index+1}")
    assert fibonacci_sequence_response.status_code == 200
    assert input in [item["value"]
                     for item in fibonacci_sequence_response.json()["items"]]
