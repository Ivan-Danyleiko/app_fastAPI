import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.schemas import ContactBase
from src.repository.contacts import (
    create_contact,
    get_all_contacts,
    get_contact,
    update_contact,
    delete_contact,
)


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(id=1, username='test_user', password="qwerty", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_all_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(id=1, name='test_name_1', email='test_email_1', user=self.user),
            Contact(id=2, name='test_name_2', email='test_email_2', user=self.user)
        ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts

        result = await get_all_contacts(limit, offset, self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact_id = 1
        contact = Contact(id=1, name='test_name', email='test_email', user=self.user)
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact

        result = await get_contact(contact_id, self.session)
        self.assertEqual(result, contact)

    async def test_create_contact(self):
        body = ContactBase(
            name='test_name',
            email='test_email',
            lastname='test_lastname',
            phone='test_phone',
            address='test_address',
            birthday='2000-01-01'
        )
        result = await create_contact(body, self.session, self.user)

        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.address, body.address)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.user, self.user)

    async def test_update_contact(self):
        contact_id = 1
        body = ContactBase(
            name='updated_name',
            email='updated_email',
            lastname='updated_lastname',
            phone='updated_phone',
            address='updated_address',
            birthday='2001-01-01'
        )
        existing_contact = Contact(id=contact_id, name='test_name', email='test_email', user=self.user)

        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = existing_contact
        self.session.execute.return_value = mocked_contact

        updated_contact = await update_contact(contact_id, body, self.session, self.user)

        self.assertIsInstance(updated_contact, Contact)
        self.assertEqual(updated_contact.name, body.name)
        self.assertEqual(updated_contact.email, body.email)
        self.assertEqual(updated_contact.lastname, body.lastname)
        self.assertEqual(updated_contact.phone, body.phone)
        self.assertEqual(updated_contact.address, body.address)
        self.assertEqual(updated_contact.birthday, body.birthday)

    async def test_delete_contact(self):
        contact_id = 1
        existing_contact = Contact(id=1, name='test_name', email='test_email', user=self.user)

        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = existing_contact
        self.session.execute.return_value = mocked_contact

        result = await delete_contact(contact_id, self.session, self.user)
        self.assertEqual(result, existing_contact)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
