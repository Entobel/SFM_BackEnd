from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PackingTypeEntity:
    """
    Represents a packing type entity with its attributes.
    This class is used to model the packing types in the system.
    """
    # Attributes corresponding to the database fields
    id: Optional[int] = None
    name: Optional[str] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def change_quantity(self, new_quantity: int):
        """
        Change the quantity of the packing type.
        :param new_quantity: The new quantity for the packing type.
        """
        self.quantity = new_quantity

    def change_name(self, new_name: str):
        """
        Change the name of the packing type.
        :param new_name: The new name for the packing type.
        """
        self.name = new_name

    def change_description(self, new_description: str):
        """
        Change the description of the packing type.
        :param new_description: The new description for the packing type.
        """
        self.description = new_description

    def change_is_active(self, new_is_active: bool):
        """
        Change the active status of the packing type.
        :param new_is_active: The new active status for the packing type.
        """
        self.is_active = new_is_active
