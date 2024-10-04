export interface sensorFileMetadata {
  id: number;
  name: string;
  content_type: string;
  size: number;
  upload_start_date: Date;
  upload_end_date?: Date;
}

export interface sensorFileMetadataResponse {
  file_metadata_records: Array<sensorFileMetadata>;
}
