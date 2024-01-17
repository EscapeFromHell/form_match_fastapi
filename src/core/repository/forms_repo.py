import logging

import email_validator
import phonenumbers
from dateutil import parser
from dateutil.parser import ParserError
from email_validator.exceptions_types import EmailSyntaxError
from fastapi import HTTPException
from phonenumbers.phonenumberutil import NumberParseException

from src.core.repository.repository import Repository
from src.core.schemas import Date, Email, MatchingTemplate, Phone
from src.utils import get_logger

logger = get_logger(log_level=logging.DEBUG)


class FormRepo(Repository):
    async def get_form(self, form_data: dict) -> MatchingTemplate | dict:
        """
        Get the matching template or return the typed form data.

        Args:
            form_data (dict): The input form data.

        Returns:
            MatchingTemplate | dict: Matching template or typed form data.
        """
        typed_form_data = await self._type_fields(form_data=form_data)
        matching_template = await self._find_matching_template(typed_form_data=typed_form_data)
        if matching_template:
            return MatchingTemplate(template_name=matching_template["name"])
        else:
            return typed_form_data

    async def _find_matching_template(self, typed_form_data: dict) -> dict | None:
        """
        Find the matching template based on the provided form data.

        Args:
            typed_form_data (dict): Typed form data.

        Returns:
            dict | None: Matching template or None if not found.
        """
        match_list = []
        async for template in self.collection.find():
            template_fields = dict(template)
            try:
                del template_fields["name"]
                del template_fields["_id"]
            except KeyError:
                logger.warning(f"The template caused an exception: {template}")
            if template_fields.items() <= typed_form_data.items():
                match_list.append(template)
        try:
            matching_template = max(match_list, key=len)
            return matching_template
        except ValueError:
            logger.info("No matching template found.")
            return None

    async def _type_fields(self, form_data: dict) -> dict:
        """
        Type the fields in the form data based on their values.

        Args:
            form_data (dict): The input form data.

        Returns:
            dict: Typed form data.
        """
        typed_fields = {}
        for field, value in form_data.items():
            field_type = await self._validate_field_type(value=value)
            typed_fields[field] = field_type
        return typed_fields

    async def _validate_field_type(self, value: str) -> str:
        """
        Validate the type of the field based on its value.

        Args:
            value (str): The value of the field.

        Returns:
            str: The validated field type.
        """
        try:
            if await self._is_valid_date(date=value):
                Date(date=value)
                field_type = "date"
            elif await self._is_valid_phone(phone=value):
                Phone(phone=value)
                field_type = "phone"
            elif await self._is_valid_email(email=value):
                Email(email=value)
                field_type = "email"
            else:
                field_type = "text"
        except ValueError as e:
            logger.error(f"The error occurred during data validation. Value: {value} is not a valid.")
            raise HTTPException(status_code=400, detail=str(e))
        return field_type

    async def _is_valid_date(self, date: str) -> bool:
        """
        Check if the provided string is a valid date.

        Args:
            date (str): The string to be checked.

        Returns:
            bool: True if the string is a valid date, False otherwise.
        """
        try:
            parser.parse(date)
            return True
        except ParserError:
            return False

    async def _is_valid_phone(self, phone: str) -> bool:
        """
        Check if the provided string is a valid phone number.

        Args:
            phone (str): The string to be checked.

        Returns:
            bool: True if the string is a valid phone number, False otherwise.
        """
        try:
            phonenumbers.parse(phone)
            return True
        except NumberParseException:
            return False

    async def _is_valid_email(self, email: str) -> bool:
        """
        Check if the provided string is a valid email address.

        Args:
            email (str): The string to be checked.

        Returns:
            bool: True if the string is a valid email address, False otherwise.
        """
        try:
            email_validator.validate_email(email, allow_empty_local=True)
            return True
        except EmailSyntaxError:
            return False
