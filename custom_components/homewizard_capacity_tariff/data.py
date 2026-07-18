"""Custom types for homewizard_capacity_tariff."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime, timedelta

    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import HomeWizardCapacityTariffApiClient
    from .coordinator import HomeWizardCapacityTariffDataUpdateCoordinator


type HomeWizardCapacityTariffConfigEntry = ConfigEntry[HomeWizardCapacityTariffData]


@dataclass
class HomeWizardCapacityTariffData:
    """Runtime data for the HomeWizard Capacity Tariff integration."""

    client: HomeWizardCapacityTariffApiClient
    coordinator: HomeWizardCapacityTariffDataUpdateCoordinator
    integration: Integration


@dataclass
class CapacityTariffData:
    """Represent parsed capacity tariff telegram data."""

    identifier: str
    timestamp: datetime
    average_peak: float
    current_month_peak: float
    current_average_demand: float
    current_month_peak_timestamp: datetime
    january_month_peak: float | None
    january_month_peak_timestamp: datetime | None
    february_month_peak: float | None
    february_month_peak_timestamp: datetime | None
    march_month_peak: float | None
    march_month_peak_timestamp: datetime | None
    april_month_peak: float | None
    april_month_peak_timestamp: datetime | None
    may_month_peak: float | None
    may_month_peak_timestamp: datetime | None
    june_month_peak: float | None
    june_month_peak_timestamp: datetime | None
    july_month_peak: float | None
    july_month_peak_timestamp: datetime | None
    august_month_peak: float | None
    august_month_peak_timestamp: datetime | None
    september_month_peak: float | None
    september_month_peak_timestamp: datetime | None
    october_month_peak: float | None
    october_month_peak_timestamp: datetime | None
    november_month_peak: float | None
    november_month_peak_timestamp: datetime | None
    december_month_peak: float | None
    december_month_peak_timestamp: datetime | None
    projected_value_history: float
    projected_value_current_power: float
    available_budget_month_peak: float
    time_remaining: timedelta
    active_power_w: float
