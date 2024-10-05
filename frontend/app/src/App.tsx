import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { FileMetadataTable } from "./components/SensorData/FileMetadataTable";
import "primeicons/primeicons.css";
import "./App.css";

function App() {
  const queryClient = new QueryClient();

  return (
    <div className="content-wrapper">
      <QueryClientProvider client={queryClient}>
        <FileMetadataTable />
      </QueryClientProvider>
    </div>
  );
}

export default App;
