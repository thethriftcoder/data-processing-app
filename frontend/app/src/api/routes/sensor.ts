import { useQuery } from "@tanstack/react-query";
import { ApiResponse, BACKEND_URL } from "../../config";
import { sensorFileMetadataResponse } from "../../schemas/sensor";

const API_PREFIX = "sensor";
const BASE_URL = `${BACKEND_URL}/${API_PREFIX}`;

export const useGetSensorFilesMetadata = () =>
  useQuery({
    queryKey: ["sensorFilesMetadata"],
    queryFn: getSensorFilesMetadata,
  });

async function getSensorFilesMetadata(): Promise<ApiResponse<sensorFileMetadataResponse>> {
  const url = new URL(BASE_URL + "/metadata");

  const response = await fetch(url);
  const jsonData = await response.json();

  if (!response.ok) {
    console.error("error getting sensor file metadata:", jsonData);
    throw new Error("Failed to get sensor file metadata");
  }

  return jsonData;
}
