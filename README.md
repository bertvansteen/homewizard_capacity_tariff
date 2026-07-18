## Installation
Copy contents of custom_components folder to your home-assistant config/custom_components folder or install through HACS. After reboot of Home-Assistant, this integration can be configured through the integration setup UI

## Exposed entities
Here is a list of exposed entities:

### Sensor

| Key | Name | Unit | Enabled by default |
| --- | --- | --- | --- |
| active_power_w | Active power | W | Yes |
| current_month_peak | Current month peak | W | Yes |
| current_month_peak_timestamp | Current month peak timestamp | - | Yes |
| interval_average_demand | Interval average demand | W | Yes |
| interval_projection_history | Interval projection (history) | W | Yes |
| interval_projection_power | Interval projection (power) | W | Yes |
| interval_allowance_month_peak | Interval allowance (current month peak) | W | Yes |
| interval_time_remaining | Interval time remaining | - | Yes (hidden by default) |
| january_peak | January peak | W | No |
| january_timestamp | January peak timestamp | - | No |
| february_peak | February peak | W | No |
| february_peak_timestamp | February peak timestamp | - | No |
| march_peak | March peak | W | No |
| march_peak_timestamp | March peak timestamp | - | No |
| april_peak | April peak | W | No |
| april_peak_timestamp | April peak timestamp | - | No |
| may_peak | May peak | W | No |
| may_peak_timestamp | May peak timestamp | - | No |
| june_peak | June peak | W | No |
| june_peak_timestamp | June peak timestamp | - | No |
| july_peak | July peak | W | No |
| july_peak_timestamp | July peak timestamp | - | No |
| august_peak | August peak | W | No |
| august_peak_timestamp | August peak timestamp | - | No |
| september_peak | September peak | W | No |
| september_peak_timestamp | September peak timestamp | - | No |
| october_peak | October peak | W | No |
| october_peak_timestamp | October peak timestamp | - | No |
| november_peak | November peak | W | No |
| november_peak_timestamp | November peak timestamp | - | No |
| december_peak | December peak | W | No |
| december_peak_timestamp | December peak timestamp | - | No |
| average_peak | Average peak | W | Yes |

Monthly peak sensors (January - December) are disabled by default to avoid cluttering the entity list; enable the ones you need from the entity settings.

### Binary sensor

| Key | Name | Enabled by default |
| --- | --- | --- |
| high_power | High power | Yes |

## Next steps

These are some next steps you may want to look into:
- Add tests to your integration, [`pytest-homeassistant-custom-component`](https://github.com/MatthewFlamm/pytest-homeassistant-custom-component) can help you get started.
- Add brand images (logo/icon).
- Create your first release.
- Share your integration on the [Home Assistant Forum](https://community.home-assistant.io/).
- Submit your integration to [HACS](https://hacs.xyz/docs/publish/start).
