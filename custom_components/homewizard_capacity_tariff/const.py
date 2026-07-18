"""Constants for homewizard_capacity_tariff."""

from logging import Logger, getLogger
from typing import Final

LOGGER: Logger = getLogger(__package__)

DOMAIN = "homewizard_capacity_tariff"
ATTRIBUTION = "Data provided by the local HomeWizard P1 meter API"

CONF_TARGET_CAPACITY: Final = "target_capacity"
CONF_MAX_CAPACITY: Final = "max_capacity"
