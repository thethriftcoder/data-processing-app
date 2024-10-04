import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { useGetSensorFilesMetadata } from "../../api/routes/sensor";

export const FileMetadataTable = () => {
  const { data, isLoading, isFetched } = useGetSensorFilesMetadata();

  const header = <div className="file-table-header">Uploaded Files Metadata</div>;

  if (isLoading) {
    console.log("loading file metadata");
  }

  if (isFetched) {
    console.log("got file metadata", data);
  }

  return (
    <div className="file-table-wrapper">
      <DataTable
        value={data?.data.file_metadata_records ?? []}
        header={header}
        tableStyle={{ minWidth: "50rem" }}
        scrollable
        scrollHeight="600px"
        showGridlines
      >
        <Column
          field="id"
          header="ID"
          style={{ width: "20px", padding: "0 20px" }}
          //   bodyStyle={{ textAlign: "center" }}
          headerStyle={{ textAlign: "center" }}
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
      </DataTable>
    </div>
  );
};
