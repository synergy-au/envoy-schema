from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class PowerForecastLog(BaseModel):
    """Represents a power forecast (either for a site known to utility server or something else) for a specific
    timestamp that was used to inform a parent CalculationLog"""

    interval_start: datetime
    interval_duration_seconds: int
    external_device_id: Optional[str]
    site_id: Optional[int]

    active_power_watts: Optional[int]
    reactive_power_var: Optional[int]


class PowerTargetLog(BaseModel):
    """Represents a power target (either for a site known to utility server or something else) for a specific
    timestamp that was the result of a CalculationLog"""

    interval_start: datetime
    interval_duration_seconds: int
    external_device_id: Optional[str]
    site_id: Optional[int]

    target_active_power_watts: Optional[int]
    target_reactive_power_var: Optional[int]


class PowerFlowLog(BaseModel):
    """Represents a log of a power flow calculation (either for a site known to utility server or something else) for
    a specific timestamp that was run at some point during the calculation process"""

    interval_start: datetime
    interval_duration_seconds: int
    external_device_id: Optional[str]

    site_id: Optional[int]
    solve_name: Optional[str]
    pu_voltage_min: Optional[Decimal]
    pu_voltage_max: Optional[Decimal]
    pu_voltage: Optional[Decimal]
    thermal_max_percent: Optional[Decimal]


class WeatherForecastLog(BaseModel):
    """Represents a weather forecast for a specific timestamp that was used to inform a parent CalculationLog"""

    air_temperature_degrees_c: Optional[Decimal]
    apparent_temperature_degrees_c: Optional[Decimal]
    dew_point_degrees_c: Optional[Decimal]
    humidity_percent: Optional[Decimal]
    cloud_cover_percent: Optional[Decimal]
    rain_probability_percent: Optional[Decimal]
    rain_mm: Optional[Decimal]
    rain_rate_mm: Optional[Decimal]
    global_horizontal_irradiance_watts_m2: Optional[Decimal]
    wind_speed_50m_km_h: Optional[Decimal]

    interval_start: datetime
    interval_duration_seconds: int


class CalculationLogRequest(BaseModel):
    """Represents the top level entity describing a single audit log of a historical calculation run.

    Calculation runs typically represent running powerflow / other model for some network based on forecast
    power/weather data (usually over multiple time steps) that may propose certain changes in DER behavior
    in order to satisfy certain network constraints"""

    calculation_interval_start: datetime
    calculation_interval_duration_seconds: int

    topology_id: Optional[str]
    external_id: Optional[str]
    description: Optional[str]
    power_forecast_creation_time: Optional[datetime]
    weather_forecast_creation_time: Optional[datetime]
    weather_forecast_location_id: Optional[str]

    power_forecast_logs: list[PowerForecastLog]
    power_target_logs: list[PowerTargetLog]
    power_flow_logs: list[PowerFlowLog]
    weather_forecast_logs: list[WeatherForecastLog]


class CalculationLogResponse(CalculationLogRequest):
    """Represents the top level entity describing a single audit log of a historical calculation run.

    Calculation runs typically represent running powerflow / other model for some network based on forecast
    power/weather data (usually over multiple time steps) that may propose certain changes in DER behavior
    in order to satisfy certain network constraints"""

    calculation_log_id: int
    created_time: datetime
