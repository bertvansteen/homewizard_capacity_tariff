"""API Client for the HomeWizard Capacity Tariff integration."""

from __future__ import annotations

import asyncio
import socket
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

import aiohttp
from dsmr_parser import obis_references, telegram_specifications
from dsmr_parser.parsers import TelegramParser

if TYPE_CHECKING:
    from dsmr_parser.objects import Telegram

from .data import CapacityTariffData


class HomeWizardCapacityTariffApiClientError(Exception):
    """Exception to indicate a general API error."""


class HomeWizardCapacityTariffApiClientCommunicationError(
    HomeWizardCapacityTariffApiClientError,
):
    """Exception to indicate a communication error."""


class HomeWizardCapacityTariffApiClientAuthenticationError(
    HomeWizardCapacityTariffApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise HomeWizardCapacityTariffApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class HomeWizardCapacityTariffApiClient:
    """HomeWizard Capacity Tariff API Client."""

    def __init__(
        self,
        ip_address: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API client."""
        self._ip_address = ip_address
        self._session = session
        self._parser = TelegramParser(telegram_specifications.BELGIUM_FLUVIUS)

    async def async_get_data(
        self, target: float, max_capacity: float
    ) -> CapacityTariffData:
        """Get data from the API."""
        try:
            async with asyncio.timeout(10):
                response = await self._session.request(
                    method="get",
                    url=f"http://{self._ip_address}/api/v1/telegram",
                )
                _verify_response_or_raise(response)
                return self.extract_data(
                    self._parser.parse(await response.text()), target, max_capacity
                )

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise HomeWizardCapacityTariffApiClientCommunicationError(
                msg,
            ) from exception
        except HomeWizardCapacityTariffApiClientError:
            raise
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise HomeWizardCapacityTariffApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise HomeWizardCapacityTariffApiClientError(
                msg,
            ) from exception

    async def async_get_deviceinfo(self) -> Any:
        """Get device information from the API."""
        try:
            async with asyncio.timeout(10):
                response = await self._session.request(
                    method="get", url=f"http://{self._ip_address}/api"
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise HomeWizardCapacityTariffApiClientCommunicationError(
                msg,
            ) from exception
        except HomeWizardCapacityTariffApiClientError:
            raise
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise HomeWizardCapacityTariffApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise HomeWizardCapacityTariffApiClientError(
                msg,
            ) from exception

    def extract_data(
        self, telegram: Telegram, target: float, max_capacity: float
    ) -> CapacityTariffData:
        """
        Return State object from API response.

        Args:
            telegram: The telegram parsed by dsmr-parser
            target: The target value for the data extraction
            max_capacity: The maximum capacity value

        Returns:
            A State object.

        """
        identifier = telegram[obis_references.BELGIUM_EQUIPMENT_IDENTIFIER]
        message_datetime = telegram[obis_references.P1_MESSAGE_TIMESTAMP]
        active_power = telegram[obis_references.CURRENT_ELECTRICITY_USAGE]
        max_demand_month = telegram[obis_references.BELGIUM_MAXIMUM_DEMAND_MONTH]
        max_demand_current_month_calc = max(max_demand_month.value, target)
        max_demand_13month = telegram[obis_references.BELGIUM_MAXIMUM_DEMAND_13_MONTHS]
        current_average_demand = telegram[
            obis_references.BELGIUM_CURRENT_AVERAGE_DEMAND
        ]

        passed_seconds = (
            message_datetime.value.minute % 15
        ) * 60 + message_datetime.value.second

        projected_value_current_power = round(
            (
                float(current_average_demand.value) * 1000
                + float(active_power.value) * 1000 / 900 * (900 - passed_seconds)
            ),
            0,
        )

        if passed_seconds == 0:
            available_budget_month_peak = float(max_demand_current_month_calc)
            projected_value_history = float(active_power.value) * 1000
        else:
            projected_value_history = round(
                current_average_demand.value / passed_seconds * 900 * 1000, 0
            )
            available_budget_month_peak = round(
                min(
                    max_capacity * 1000,
                    (
                        (
                            float(max_demand_current_month_calc)
                            - float(current_average_demand.value)
                        )
                        * 900
                        / (900 - passed_seconds)
                        * 1000
                    ),
                ),
                0,
            )

        peaks = [0.0] * 12
        peakdates: list[datetime | None] = [None] * 12

        for x in max_demand_13month:
            if x is not None and x.occurred is not None:
                peakdates[x.occurred.month - 1] = x.occurred
                peaks[x.occurred.month - 1] = float(x.value) * 1000

        known_peaks = [peak for peak in peaks if peak > 0]
        average_peak = sum(known_peaks) / len(known_peaks) if known_peaks else 0.0

        return CapacityTariffData(
            identifier=identifier,
            timestamp=message_datetime.value,
            average_peak=average_peak,
            current_month_peak=float(max_demand_month.value) * 1000,
            current_month_peak_timestamp=max_demand_month.datetime,
            current_average_demand=float(current_average_demand.value) * 1000,
            january_month_peak=peaks[0],
            january_month_peak_timestamp=peakdates[0],
            february_month_peak=peaks[1],
            february_month_peak_timestamp=peakdates[1],
            march_month_peak=peaks[2],
            march_month_peak_timestamp=peakdates[2],
            april_month_peak=peaks[3],
            april_month_peak_timestamp=peakdates[3],
            may_month_peak=peaks[4],
            may_month_peak_timestamp=peakdates[4],
            june_month_peak=peaks[5],
            june_month_peak_timestamp=peakdates[5],
            july_month_peak=peaks[6],
            july_month_peak_timestamp=peakdates[6],
            august_month_peak=peaks[7],
            august_month_peak_timestamp=peakdates[7],
            september_month_peak=peaks[8],
            september_month_peak_timestamp=peakdates[8],
            october_month_peak=peaks[9],
            october_month_peak_timestamp=peakdates[9],
            november_month_peak=peaks[10],
            november_month_peak_timestamp=peakdates[10],
            december_month_peak=peaks[11],
            december_month_peak_timestamp=peakdates[11],
            projected_value_history=projected_value_history,
            available_budget_month_peak=available_budget_month_peak,
            time_remaining=timedelta(seconds=(900 - passed_seconds)),
            projected_value_current_power=projected_value_current_power,
            active_power_w=active_power.value * 1000,
        )
