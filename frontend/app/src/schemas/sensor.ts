export interface sensorFileMetadata {
  id: number;
  name: string;
  content_type: string;
  size: number;
  upload_start_date: Date;
  upload_end_date: Date | null;
}

interface hourlyDataValue {
  time: Date;
  value: number | null;
}

export interface sensorData {
  id: number;
  file_metadata_id: number;
  elevation: number;
  generationtime_ms: number;
  longitude: number;
  latitude: number;
  utc_offset_seconds: number;
  timezone: string;
  timezone_abbreviation: string;
  hourly_wind_speeds_100m: hourlyDataValue[];
  hourly_wind_directions_100m: hourlyDataValue[];
  hourly_temperatures: hourlyDataValue[];
  hourly_humidities: hourlyDataValue[];
  hourly_dew_points: hourlyDataValue[];
  hourly_apparent_temperatures: hourlyDataValue[];
  hourly_precipitations: hourlyDataValue[];
  hourly_rains: hourlyDataValue[];
  hourly_snowfalls: hourlyDataValue[];
  hourly_snow_depths: hourlyDataValue[];
  hourly_pressures_msl: hourlyDataValue[];
  hourly_surface_pressures: hourlyDataValue[];
  hourly_cloud_covers: hourlyDataValue[];
}

export interface sensorFileMetadataResponse {
  file_metadata_records: Array<sensorFileMetadata>;
}

export interface sensorDataResponse {
  sensor_data: sensorData;
}
