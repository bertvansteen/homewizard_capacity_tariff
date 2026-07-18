"""Adds config flow for HomeWizard Capacity Tariff."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import (
    HomeWizardCapacityTariffApiClient,
    HomeWizardCapacityTariffApiClientAuthenticationError,
    HomeWizardCapacityTariffApiClientCommunicationError,
    HomeWizardCapacityTariffApiClientError,
)
from .const import CONF_MAX_CAPACITY, CONF_TARGET_CAPACITY, DOMAIN, LOGGER

_IP_ADDRESS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): selector.TextSelector(
            selector.TextSelectorConfig(
                type=selector.TextSelectorType.TEXT,
            ),
        ),
        vol.Required(CONF_TARGET_CAPACITY, default=2.5): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=1,
                max=100,
                step=0.1,
                mode=selector.NumberSelectorMode.BOX,
                translation_key="target_capacity",
            )
        ),
        vol.Required(
            CONF_MAX_CAPACITY, default=(20 * 3 * 230 / 1000)
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=1,
                max=100,
                step=0.1,
                mode=selector.NumberSelectorMode.BOX,
                translation_key="max_capacity",
            )
        ),
    }
)


class HomeWizardCapacityTariffFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HomeWizard Capacity Tariff."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors: dict[str, str] = {}
        if user_input is not None:
            serial, errors = await self._async_test_connection(
                ip_address=user_input[CONF_IP_ADDRESS]
            )
            if serial is not None:
                await self.async_set_unique_id(
                    unique_id=f"homewizard_capacity_tariff_{serial}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"HomeWizard Capacity Tariff ({serial})",
                    data=user_input,
                )

        integration = async_get_loaded_integration(self.hass, DOMAIN)
        assert integration.documentation is not None, (  # noqa: S101
            "Integration documentation URL is not set in manifest.json"
        )

        return self.async_show_form(
            step_id="user",
            description_placeholders={
                "documentation_url": integration.documentation,
            },
            data_schema=_IP_ADDRESS_SCHEMA,
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle reconfiguration of the integration."""
        errors: dict[str, str] = {}
        reconfigure_entry = self._get_reconfigure_entry()

        if user_input:
            serial, errors = await self._async_test_connection(
                ip_address=user_input[CONF_IP_ADDRESS]
            )
            if serial is not None:
                await self.async_set_unique_id(
                    unique_id=f"homewizard_capacity_tariff_{serial}"
                )
                self._abort_if_unique_id_mismatch(reason="wrong_device")
                return self.async_update_reload_and_abort(
                    reconfigure_entry,
                    data_updates=user_input,
                )
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_IP_ADDRESS_SCHEMA,
            description_placeholders={
                "title": reconfigure_entry.title,
            },
            errors=errors,
        )

    async def _async_test_connection(
        self, ip_address: str
    ) -> tuple[str | None, dict[str, str]]:
        """Validate the connection and return the device serial, if any."""
        client = HomeWizardCapacityTariffApiClient(
            ip_address=ip_address,
            session=async_create_clientsession(self.hass),
        )
        try:
            device_info = await client.async_get_deviceinfo()
            serial = device_info["serial"]
        except HomeWizardCapacityTariffApiClientAuthenticationError as exception:
            LOGGER.warning(exception)
            return None, {"base": "auth"}
        except HomeWizardCapacityTariffApiClientCommunicationError as exception:
            LOGGER.error(exception)
            return None, {"base": "connection"}
        except (
            HomeWizardCapacityTariffApiClientError,
            KeyError,
            TypeError,
        ) as exception:
            LOGGER.exception(exception)
            return None, {"base": "unknown"}
        else:
            return serial, {}
