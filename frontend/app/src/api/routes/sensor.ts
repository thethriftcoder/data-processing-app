import { useMutation, useQuery } from "@tanstack/react-query";
import { ApiResponse, AUTH_HEADER, BACKEND_URL } from "../../config";
import { sensorDataResponse, sensorFileMetadataResponse } from "../../schemas/sensor";

const API_PREFIX = "sensor";
const BASE_URL = `${BACKEND_URL}/${API_PREFIX}`;

type getSensorDataProps = {
  fileMetadataId: number;
};

export const useGetSensorFilesMetadata = () =>
  useQuery({
    queryKey: ["sensorFilesMetadata"],
    queryFn: getSensorFilesMetadata,
  });

export const useGetSensorData = () =>
  useMutation({
    mutationKey: ["sensorData"],
    mutationFn: ({ fileMetadataId }: getSensorDataProps) => getSensorData(fileMetadataId),
  });

async function getSensorFilesMetadata(): Promise<ApiResponse<sensorFileMetadataResponse>> {
  const url = new URL(BASE_URL + "/metadata");

  const response = await fetch(url, {
    headers: { Authorization: AUTH_HEADER },
  });
  const jsonData = await response.json();

  if (!response.ok) {
    console.error("error getting sensor file metadata:", jsonData);
    throw new Error("Failed to get sensor file metadata");
  }

  return jsonData;
}

async function getSensorData(fileMetadataId: number): Promise<ApiResponse<sensorDataResponse>> {
  const url = new URL(BASE_URL + "/data/" + fileMetadataId);

  const response = await fetch(url, {
    headers: { Authorization: AUTH_HEADER },
  });
  const jsonData = await response.json();

  if (!response.ok) {
    console.error("error getting sensor data:", jsonData);
    throw new Error(`Failed to get sensor data for file metadata ID: ${fileMetadataId}`);
  }

  return jsonData;
}
