import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  ZAxis,
} from "recharts";

const PriceChart = ({ data, events, changepoint, detailed = false }) => {
  if (!data || data.length === 0) {
    return <div className="chart-placeholder">No price data available</div>;
  }

  const eventMarkers =
    events?.map((event) => ({
      x: event.Date,
      type: event.Event_Type,
      desc: event.Description,
    })) || [];

  return (
    <div className="price-chart">
      <ResponsiveContainer width="100%" height={detailed ? 500 : 400}>
        <LineChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="Date"
            angle={-45}
            textAnchor="end"
            height={80}
            tick={{ fontSize: 12 }}
          />
          <YAxis
            label={{
              value: "Price (USD/barrel)",
              angle: -90,
              position: "insideLeft",
            }}
          />
          <Tooltip
            contentStyle={{ backgroundColor: "#fff", border: "1px solid #ccc" }}
            formatter={(value) => [`$${value.toFixed(2)}`, "Price"]}
          />
          <Legend />

          <Line
            type="monotone"
            dataKey="Price"
            stroke="#1f77b4"
            strokeWidth={2}
            dot={false}
            name="Brent Price"
          />

          {changepoint && (
            <ReferenceLine
              x={changepoint.change_point_date}
              stroke="red"
              strokeWidth={3}
              strokeDasharray="5 5"
              label={{
                value: `Change Point: ${changepoint.change_point_date}`,
                position: "top",
                fill: "red",
                fontSize: 12,
              }}
            />
          )}
        </LineChart>
      </ResponsiveContainer>

      {detailed && (
        <div className="chart-legend">
          <div className="legend-item">
            <span
              className="legend-color"
              style={{ backgroundColor: "#1f77b4" }}
            ></span>
            <span>Brent Oil Price</span>
          </div>
          <div className="legend-item">
            <span
              className="legend-color"
              style={{
                backgroundColor: "red",
                border: "2px dashed red",
                background: "transparent",
              }}
            ></span>
            <span>
              Detected Change Point ({changepoint?.change_point_date})
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default PriceChart;
