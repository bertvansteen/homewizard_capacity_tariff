"""Binary sensor platform for homewizard_capacity_tariff."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import HomeWizardCapacityTariffEntity

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import HomeWizardCapacityTariffDataUpdateCoordinator
    from .data import CapacityTariffData, HomeWizardCapacityTariffConfigEntry

HIGH_POWER_THRESHOLD_W = 100


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: HomeWizardCapacityTariffConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        HomeWizardCapacityTariffBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in BINARY_SENSORS
    )


@dataclass(frozen=True)
class HomeWizardBinarySensorEntityDescriptionMixin:
    """Mixin values for HomeWizard binary sensor entities."""

    is_on_fn: Callable[[CapacityTariffData], bool]


@dataclass(frozen=True)
class HomeWizardCapacityTariffBinarySensorEntityDescription(
    BinarySensorEntityDescription, HomeWizardBinarySensorEntityDescriptionMixin
):
    """Class describing HomeWizard Capacity Tariff binary sensor entities."""


BINARY_SENSORS = (
    HomeWizardCapacityTariffBinarySensorEntityDescription(
        key="high_power",
        translation_key="high_power",
        device_class=BinarySensorDeviceClass.POWER,
        is_on_fn=lambda telegram: telegram.active_power_w > HIGH_POWER_THRESHOLD_W,
    ),
)


class HomeWizardCapacityTariffBinarySensor(
    HomeWizardCapacityTariffEntity, BinarySensorEntity
):
    """homewizard_capacity_tariff binary_sensor class."""

    _attr_has_entity_name = True

    entity_description: HomeWizardCapacityTariffBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: HomeWizardCapacityTariffDataUpdateCoordinator,
        entity_description: HomeWizardCapacityTariffBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.unique_id}_{entity_description.key}"
        )

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self.entity_description.is_on_fn(self.coordinator.data)
