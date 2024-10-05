export interface SensorFileMetadata {
  id: number;
  name: string;
  content_type: string;
  size: number;
  upload_start_date: Date;
  upload_end_date: Date | null;
}

export interface HourlyDataValue {
  time: Date;
  value: number | null;
}

interface HourlyUnits {
  sensor_data_id: number;
  time: string;
  relative_humidity_2m: string;
  apparent_temperature: string;
  rain: string;
  snow_depth: string;
  surface_pressure: string;
  wind_speed_100m: string;
  id: number;
  temperature_2m: string;
  dew_point_2m: string;
  precipitation: string;
  snowfall: string;
  pressure_msl: string;
  cloud_cover: string;
  wind_direction_100m: string;
}

export interface SensorData {
  id: number;
  file_metadata_id: number;
  elevation: number;
  generationtime_ms: number;
  longitude: number;
  latitude: number;
  utc_offset_seconds: number;
  timezone: string;
  timezone_abbreviation: string;
  hourly_units: HourlyUnits;
  hourly_wind_speeds_100m: HourlyDataValue[];
  hourly_wind_directions_100m: HourlyDataValue[];
  hourly_temperatures: HourlyDataValue[];
  hourly_humidities: HourlyDataValue[];
  hourly_dew_points: HourlyDataValue[];
  hourly_apparent_temperatures: HourlyDataValue[];
  hourly_precipitations: HourlyDataValue[];
  hourly_rains: HourlyDataValue[];
  hourly_snowfalls: HourlyDataValue[];
  hourly_snow_depths: HourlyDataValue[];
  hourly_pressures_msl: HourlyDataValue[];
  hourly_surface_pressures: HourlyDataValue[];
  hourly_cloud_covers: HourlyDataValue[];
}

export interface SensorFileMetadataResponse {
  file_metadata_records: Array<SensorFileMetadata>;
}

export interface SensorDataResponse {
  sensor_data: SensorData;
}
