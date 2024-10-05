import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
} from "chart.js";
import { HourlyDataValue, SensorData } from "../../schemas/sensor";
import { Dialog } from "primereact/dialog";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

// Map over all hourly data values to create corresponding datasets
function createDataset(dataArray: HourlyDataValue[], label: string, unit: string, color: string, yAxisID: string) {
  return {
    label: `${label} (${unit})`, // Updated to include the unit correctly
    data: dataArray.map((data) => ({
      x: data.time,
      y: data.value ?? 0,
    })),
    borderColor: color,
    backgroundColor: `${color}0.2`,
    yAxisID: yAxisID,
  };
}

interface ChartProps {
  sensorData: SensorData;
}

const SensorDataChart = ({ sensorData }: ChartProps) => {
  console.warn("rendering chart data", sensorData);
  // Map the data for time and values from SensorData for a specific parameter
  const times = sensorData.hourly_temperatures.map((data) => data.time);

  // Labels for axes from HourlyUnits
  const {
    temperature_2m,
    relative_humidity_2m,
    pressure_msl,
    dew_point_2m,
    cloud_cover,
    // precipitation,
    // rain,
    // snowfall,
    // snow_depth,
    // surface_pressure,
  } = sensorData.hourly_units;

  const data = {
    labels: times,
    datasets: [
      createDataset(sensorData.hourly_temperatures, `Temperature`, temperature_2m, "rgba(255, 99, 132, 1)", "y1"),
      createDataset(sensorData.hourly_humidities, `Humidity`, relative_humidity_2m, "rgba(54, 162, 235, 1)", "y2"),
      createDataset(sensorData.hourly_pressures_msl, `Pressure`, pressure_msl, "rgba(75, 192, 192, 1)", "y3"),
      createDataset(sensorData.hourly_dew_points, `Dew Point`, dew_point_2m, "rgba(255, 206, 86, 1)", "y4"),
      createDataset(sensorData.hourly_cloud_covers, `Cloud Cover`, cloud_cover, "rgba(255, 159, 64, 1)", "y10"),
      //   createDataset(sensorData.hourly_precipitations, `Precipitation`, precipitation, "pink", "y5"),
      //   createDataset(sensorData.hourly_rains, `Rain`, rain, "rgba(255, 159, 64, 1)", "y6"),
      //   createDataset(sensorData.hourly_snowfalls, `Snowfall`, snowfall, "rgba(255, 99, 132, 1)", "y7"),
      //   createDataset(sensorData.hourly_snow_depths, `Snow Depth`, snow_depth, "rgba(54, 162, 235, 1)", "y8"),
      //   createDataset(
      //     sensorData.hourly_surface_pressures,
      //     `Surface Pressure`,
      //     surface_pressure,
      //     "rgba(75, 192, 192, 1)",
      //     "y9"
      //   ),
    ],
  };

  const options: ChartOptions = {
    responsive: true,
    interaction: {
      mode: "index",
      intersect: true,
    },
    scales: {
      x: {
        type: "category",
        title: {
          display: true,
          text: "Time",
        },
      },
      y1: { display: true, min: 0 },
      y2: { display: true, min: 0 },
      y3: { display: true, min: 0 },
      y4: { display: true, min: 0 },
      y10: { display: false, min: 0 },
      //   y5: { display: true, min: 0 },
      //   y6: { display: false, min: 0 },
      //   y7: { display: false, min: 0 },
      //   y8: { display: false, min: 0 },
      //   y9: { display: false, min: 0 },
    },
  };

  //@ts-expect-error options works fine
  return <Line data={data} options={options} />;
};

interface SensorDataDialogProps {
  sensorData?: SensorData;
  visible: boolean;
  onHide: () => void;
}

export const SensorDataDialog = ({ sensorData, visible, onHide }: SensorDataDialogProps) => {
  if (sensorData) {
    console.log("rendering dialog");
  }

  return (
    <Dialog
      header="Sensor Data"
      visible={visible}
      onHide={onHide}
      modal
      style={{ backgroundColor: "black" }}
      maximized={true}
    >
      {sensorData && <SensorDataChart sensorData={sensorData} />}
    </Dialog>
  );
};
