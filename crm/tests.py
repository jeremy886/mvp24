# crm/tests.py

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Record


@pytest.mark.django_db
def test_record_creation():
    # Create a new record instance
    record = Record.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        address="123 Main St",
        city="Anytown",
        state="Anystate",
        zipcode="12345"
    )

    # Assert that the record was created correctly
    assert record.first_name == "John"
    assert record.last_name == "Doe"
    assert record.email == "john.doe@example.com"
    assert record.phone == "1234567890"
    assert record.address == "123 Main St"
    assert record.city == "Anytown"
    assert record.state == "Anystate"
    assert record.zipcode == "12345"

    # Verify the record count in the database
    assert Record.objects.count() == 1


@pytest.mark.django_db
def test_record_str_representation():
    # Create a new record instance
    record = Record.objects.create(
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        phone="0987654321",
        address="456 Elm St",
        city="Othertown",
        state="Otherstate",
        zipcode="67890"
    )

    # Assert that the __str__ method returns the correct string representation
    assert str(record) == "Jane Smith"


@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'crm/home.html' in [t.name for t in response.templates]
    assert response.context['records']['developer'] == "Jeremy Chen"


@pytest.mark.django_db
def test_record_list_view(client):
    Record.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890",
                          address="123 Main St", city="Anytown", state="Anystate", zipcode="12345")
    response = client.get(reverse('record_list'))
    assert response.status_code == 200
    assert 'crm/record_list.html' in [t.name for t in response.templates]
    assert len(response.context['records']) == 1


@pytest.mark.django_db
def test_record_detail_view(client):
    record = Record.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890",
                                   address="123 Main St", city="Anytown", state="Anystate", zipcode="12345")
    response = client.get(reverse('record_detail', args=[record.pk]))
    assert response.status_code == 200
    assert 'crm/record_detail.html' in [t.name for t in response.templates]
    assert response.context['record'] == record


@pytest.mark.django_db
def test_record_create_view(client):
    # Create a user and log in
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    # Test GET request
    response = client.get(reverse('record_create'))
    assert response.status_code == 200
    assert 'crm/record_form.html' in [t.name for t in response.templates]

    # Test POST request
    response = client.post(reverse('record_create'), {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'phone': '0987654321',
        'address': '456 Elm St',
        'city': 'Othertown',
        'state': 'Otherstate',
        'zipcode': '67890',
    })
    assert response.status_code == 302  # Redirect after successful creation
    assert Record.objects.count() == 1


@pytest.mark.django_db
def test_record_update_view(client):
    # Create a user and log in
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    record = Record.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890",
                                   address="123 Main St", city="Anytown", state="Anystate", zipcode="12345")

    # Test GET request
    response = client.get(reverse('record_update', args=[record.pk]))
    assert response.status_code == 200
    assert 'crm/record_form.html' in [t.name for t in response.templates]

    # Test POST request
    response = client.post(reverse('record_update', args=[record.pk]), {
        'first_name': 'John',
        'last_name': 'Smith',
        'email': 'john.smith@example.com',
        'phone': '1234567890',
        'address': '123 Main St',
        'city': 'Anytown',
        'state': 'Anystate',
        'zipcode': '12345',
    })
    assert response.status_code == 302  # Redirect after successful update
    record.refresh_from_db()
    assert record.last_name == "Smith"
    assert record.email == "john.smith@example.com"


@pytest.mark.django_db
def test_record_delete_view(client):
    # Create a user and log in
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    record = Record.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890",
                                   address="123 Main St", city="Anytown", state="Anystate", zipcode="12345")

    # Test GET request
    response = client.get(reverse('record_delete', args=[record.pk]))
    assert response.status_code == 200
    assert 'crm/record_confirm_delete.html' in [t.name for t in response.templates]

    # Test POST request
    response = client.post(reverse('record_delete', args=[record.pk]))
    assert response.status_code == 302  # Redirect after successful deletion
    assert Record.objects.count() == 0
