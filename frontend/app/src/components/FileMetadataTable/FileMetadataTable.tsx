// import React, { useState } from "react";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";

const tableData = [
  {
    name: "small_data.json",
    id: 4,
    contentType: "application/json",
    size: 7648,
    uploadStartDate: "2024-10-03T05:34:03.049648",
    uploadEndDate: "2024-10-03T05:34:04.049648",
  },
  {
    name: "small_data.json",
    id: 5,
    contentType: "application/json",
    size: 7648,
    uploadStartDate: "2024-10-03T05:34:03.049648",
    uploadEndDate: "2024-10-03T05:34:04.049648",
  },
  {
    name: "small_data.json",
    id: 6,
    contentType: "application/json",
    size: 7648,
    uploadStartDate: "2024-10-03T05:34:03.049648",
    uploadEndDate: "2024-10-03T05:34:04.049648",
  },
];

export const FileMetadataTable = () => {
  const header = <div className="file-table-header">Uploaded Files Metadata</div>;

  return (
    <div className="file-table-wrapper">
      <DataTable
        value={tableData}
        header={header}
        tableStyle={{ minWidth: "50rem", width: "85%", borderColor: "blue" }}
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
          field="contentType"
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
          field="uploadStartDate"
          header="File Uploaded At"
          style={{ width: "300px", padding: "0 20px" }}
          headerStyle={{ textAlign: "center" }}
        />
        <Column
          field="uploadEndDate"
          header="File Processed At"
          style={{ width: "300px", padding: "0 20px" }}
          headerStyle={{ textAlign: "center" }}
        />
      </DataTable>
    </div>
  );
};
