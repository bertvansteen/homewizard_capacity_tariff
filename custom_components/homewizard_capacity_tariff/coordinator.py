"""DataUpdateCoordinator for homewizard_capacity_tariff."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from custom_components.homewizard_capacity_tariff.const import (
    CONF_MAX_CAPACITY,
    CONF_TARGET_CAPACITY,
)

from .api import (
    HomeWizardCapacityTariffApiClientAuthenticationError,
    HomeWizardCapacityTariffApiClientError,
)
from .data import CapacityTariffData

if TYPE_CHECKING:
    from .data import HomeWizardCapacityTariffConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class HomeWizardCapacityTariffDataUpdateCoordinator(
    DataUpdateCoordinator[CapacityTariffData]
):
    """Class to manage fetching data from the API."""

    config_entry: HomeWizardCapacityTariffConfigEntry

    async def _async_update_data(self) -> CapacityTariffData:
        """Update data from the API."""
        try:
            self.logger.debug(
                "Target capacity: %s, Max capacity: %s",
                float(self.config_entry.data[CONF_TARGET_CAPACITY]),
                float(self.config_entry.data[CONF_MAX_CAPACITY]),
            )
            return await self.config_entry.runtime_data.client.async_get_data(
                float(self.config_entry.data[CONF_TARGET_CAPACITY]),
                float(self.config_entry.data[CONF_MAX_CAPACITY]),
            )
        except HomeWizardCapacityTariffApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except HomeWizardCapacityTariffApiClientError as exception:
            raise UpdateFailed(exception) from exception
