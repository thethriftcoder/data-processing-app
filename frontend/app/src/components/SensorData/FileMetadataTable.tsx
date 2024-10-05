import { DataTable, DataTableValue } from "primereact/datatable";
import { Column } from "primereact/column";
import { useGetSensorData, useGetSensorFilesMetadata } from "../../api/routes/sensor";
import { Button } from "primereact/button";
import { useState } from "react";
import { SensorFileMetadata } from "../../schemas/sensor";
import { SensorDataDialog } from "./SensorDataChart";

export const FileMetadataTable = () => {
  const [selectedRow, setSelectedRow] = useState<DataTableValue | null>(null);
  const [showChartData, setShowChartData] = useState(false);

  const { data, refetch, isFetching, isFetched } = useGetSensorFilesMetadata();
  const getSensorDataMutation = useGetSensorData();

  if (isFetching) {
    console.log("getting file metadata");
  }

  if (isFetched && !selectedRow) {
    console.log("got file metadata", data);
  }

  const hideChartDataModal = () => setShowChartData(false);

  const header = (
    <div className="file-table-header">
      <span>Uploaded Files Metadata</span>
      <Button
        icon="pi pi-refresh"
        label="Refresh"
        rounded
        raised
        size="small"
        onClick={() => {
          refetch();
          setSelectedRow(null);
        }}
        disabled={isFetching}
      />
    </div>
  );

  const actionButtons = (rowData: SensorFileMetadata) => (
    <div className="file-table-actions">
      <Button
        icon="pi pi-chart-bar"
        title="Show Sensor Data Graph"
        rounded
        size="small"
        disabled={isFetching}
        className="sensor-graph-button"
        onClick={() => {
          getSensorDataMutation.mutate({ fileMetadataId: rowData.id });
          setShowChartData(true);
        }}
      />
    </div>
  );

  return (
    <div className="file-table-wrapper">
      <SensorDataDialog
        sensorData={getSensorDataMutation.data?.data.sensor_data}
        visible={showChartData}
        onHide={hideChartDataModal}
      />

      <DataTable
        value={data?.data.file_metadata_records ?? []}
        header={header}
        tableStyle={{ minWidth: "50rem" }}
        scrollable
        scrollHeight="600px"
        showGridlines
        // selectionMode={"radiobutton"}
        selection={selectedRow}
        onSelectionChange={(e) => setSelectedRow(e.value)}
        dataKey={"id"}
      >
        <Column
          field="id"
          header="ID"
          style={{ width: "20px", padding: "0 20px" }}
          headerStyle={{ textAlign: "center" }}
          //   selectionMode={"single"}
        />
        <Column
          field="name"
          header="File Name"
          style={{ width: "175px", padding: "0 20px" }}
          headerStyle={{ textAlign: "center" }}
        />
        <Column
          field="content_type"
          header="Content Type"
          style={{ width: "150px", padding: "0 20px" }}
          headerStyle={{ textAlign: "center" }}
        />
        <Column
          field="size"
          header="File Size"
          style={{ width: "125px", padding: "0 20px" }}
          headerStyle={{ textAlign: "center" }}
        />
        <Column
          field="upload_start_date"
          header="File Uploaded At"
          style={{ width: "300px", padding: "0 20px" }}
          headerStyle={{ textAlign: "center" }}
        />
        <Column
          field="upload_end_date"
          header="File Processed At"
          style={{ width: "300px", padding: "0 20px" }}
          headerStyle={{ textAlign: "center" }}
          body={(rowData) => rowData.upload_end_date || "N/A"}
        />
        <Column body={actionButtons} header="Actions" />
      </DataTable>
    </div>
  );
};
