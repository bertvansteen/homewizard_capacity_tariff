"""Sensor platform for homewizard_capacity_tariff."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfPower

from .entity import HomeWizardCapacityTariffEntity

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime, timedelta

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import HomeWizardCapacityTariffDataUpdateCoordinator
    from .data import CapacityTariffData, HomeWizardCapacityTariffConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: HomeWizardCapacityTariffConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        HomeWizardCapacityTariffSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in SENSORS
    )


class HomeWizardCapacityTariffSensor(HomeWizardCapacityTariffEntity, SensorEntity):
    """homewizard_capacity_tariff Sensor class."""

    _attr_has_entity_name = True

    entity_description: HomeWizardCapacityTariffSensorEntityDescription

    def __init__(
        self,
        coordinator: HomeWizardCapacityTariffDataUpdateCoordinator,
        entity_description: HomeWizardCapacityTariffSensorEntityDescription,
    ) -> None:
        """Initialize Sensor Domain."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.unique_id}_{entity_description.key}"
        )

    @property
    def native_value(self) -> float | int | str | datetime | timedelta | None:
        """Return the sensor value."""
        return self.entity_description.value_fn(self.coordinator.data)


@dataclass(frozen=True)
class HomeWizardEntityDescriptionMixin:
    """Mixin values for HomeWizard entities."""

    value_fn: Callable[
        [CapacityTariffData], float | int | str | datetime | timedelta | None
    ]


@dataclass(frozen=True)
class HomeWizardCapacityTariffSensorEntityDescription(
    SensorEntityDescription, HomeWizardEntityDescriptionMixin
):
    """Class describing  sensor entities."""


SENSORS = (
    HomeWizardCapacityTariffSensorEntityDescription(
        key="active_power_w",
        translation_key="active_power_w",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda telegram: telegram.active_power_w,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="current_month_peak",
        translation_key="current_month_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda telegram: telegram.current_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="current_month_peak_timestamp",
        translation_key="current_month_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda telegram: telegram.current_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="interval_average_demand",
        translation_key="interval_average_demand",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda telegram: telegram.current_average_demand,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="interval_projection_history",
        translation_key="interval_projection_history",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda telegram: telegram.projected_value_history,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="interval_projection_power",
        translation_key="interval_projection_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda telegram: telegram.projected_value_current_power,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="interval_allowance_month_peak",
        translation_key="interval_allowance_month_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda telegram: telegram.available_budget_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="interval_time_remaining",
        translation_key="interval_time_remaining",
        value_fn=lambda telegram: telegram.time_remaining,
        entity_registry_visible_default=False,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="january_peak",
        translation_key="january_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.january_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="january_timestamp",
        translation_key="january_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.january_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="february_peak",
        translation_key="february_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.february_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="february_peak_timestamp",
        translation_key="february_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.february_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="march_peak",
        translation_key="march_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.march_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="march_peak_timestamp",
        translation_key="march_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.march_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="april_peak",
        translation_key="april_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.april_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="april_peak_timestamp",
        translation_key="april_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.april_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="may_peak",
        translation_key="may_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.may_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="may_peak_timestamp",
        translation_key="may_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.may_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="june_peak",
        translation_key="june_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.june_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="june_peak_timestamp",
        translation_key="june_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.june_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="july_peak",
        translation_key="july_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.july_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="july_peak_timestamp",
        translation_key="july_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.july_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="august_peak",
        translation_key="august_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.august_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="august_peak_timestamp",
        translation_key="august_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.august_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="september_peak",
        translation_key="september_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.september_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="september_peak_timestamp",
        translation_key="september_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.september_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="october_peak",
        translation_key="october_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.october_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="october_peak_timestamp",
        translation_key="october_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.october_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="november_peak",
        translation_key="november_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.november_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="november_peak_timestamp",
        translation_key="november_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.november_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="december_peak",
        translation_key="december_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.december_month_peak,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="december_peak_timestamp",
        translation_key="december_peak_timestamp",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda telegram: telegram.december_month_peak_timestamp,
    ),
    HomeWizardCapacityTariffSensorEntityDescription(
        key="average_peak",
        translation_key="average_peak",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda telegram: telegram.average_peak or None,
    ),
)
