from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class PowerForecastLog(BaseModel):
    """Represents a power forecast (either for a site known to utility server or something else) for a specific
    timestamp that was used to inform a parent CalculationLog"""

    interval_start: datetime
    interval_duration_seconds: int
    external_device_id: Optional[str] = None
    site_id: Optional[int] = None

    active_power_watts: Optional[int] = None
    reactive_power_var: Optional[int] = None


class PowerTargetLog(BaseModel):
    """Represents a power target (either for a site known to utility server or something else) for a specific
    timestamp that was the result of a CalculationLog"""

    interval_start: datetime
    interval_duration_seconds: int
    external_device_id: Optional[str] = None
    site_id: Optional[int] = None

    target_active_power_watts: Optional[int] = None
    target_reactive_power_var: Optional[int] = None


class PowerFlowLog(BaseModel):
    """Represents a log of a power flow calculation (either for a site known to utility server or something else) for
    a specific timestamp that was run at some point during the calculation process"""

    interval_start: datetime
    interval_duration_seconds: int
    external_device_id: Optional[str] = None

    site_id: Optional[int] = None
    solve_name: Optional[str] = None
    pu_voltage_min: Optional[Decimal] = None
    pu_voltage_max: Optional[Decimal] = None
    pu_voltage: Optional[Decimal] = None
    thermal_max_percent: Optional[Decimal] = None


class WeatherForecastLog(BaseModel):
    """Represents a weather forecast for a specific timestamp that was used to inform a parent CalculationLog"""

    air_temperature_degrees_c: Optional[Decimal] = None
    apparent_temperature_degrees_c: Optional[Decimal] = None
    dew_point_degrees_c: Optional[Decimal] = None
    humidity_percent: Optional[Decimal] = None
    cloud_cover_percent: Optional[Decimal] = None
    rain_probability_percent: Optional[Decimal] = None
    rain_mm: Optional[Decimal] = None
    rain_rate_mm: Optional[Decimal] = None
    global_horizontal_irradiance_watts_m2: Optional[Decimal] = None
    wind_speed_50m_km_h: Optional[Decimal] = None

    interval_start: datetime
    interval_duration_seconds: int


class CalculationLogRequest(BaseModel):
    """Represents the top level entity describing a single audit log of a historical calculation run.

    Calculation runs typically represent running powerflow / other model for some network based on forecast
    power/weather data (usually over multiple time steps) that may propose certain changes in DER behavior
    in order to satisfy certain network constraints"""

    calculation_interval_start: datetime
    calculation_interval_duration_seconds: int

    topology_id: Optional[str] = None
    external_id: Optional[str] = None
    description: Optional[str] = None
    power_forecast_creation_time: Optional[datetime] = None
    weather_forecast_creation_time: Optional[datetime] = None
    weather_forecast_location_id: Optional[str] = None

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
