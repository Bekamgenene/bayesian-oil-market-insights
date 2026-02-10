import React from "react";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

const EventTimeline = ({ events, changepoint }) => {
  if (!events || events.length === 0) {
    return <div className="chart-placeholder">No events data available</div>;
  }

  // Event type colors
  const eventColors = {
    OPEC_Decision: "#2ecc71",
    Geopolitical: "#e74c3c",
    Economic_Shock: "#f39c12",
    default: "#95a5a6",
  };

  // Prepare data for scatter plot (y-axis represents event type)
  const scatterData = events.map((event, idx) => ({
    date: event.Date,
    y:
      event.Event_Type === "OPEC_Decision"
        ? 3
        : event.Event_Type === "Geopolitical"
          ? 2
          : event.Event_Type === "Economic_Shock"
            ? 1
            : 0,
    type: event.Event_Type,
    description: event.Description,
    impact: event.Expected_Impact,
    color: eventColors[event.Event_Type] || eventColors.default,
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="custom-tooltip">
          <p className="tooltip-date">
            <strong>{data.date}</strong>
          </p>
          <p className="tooltip-type">Type: {data.type}</p>
          <p className="tooltip-desc">{data.description}</p>
          <p className="tooltip-impact">Impact: {data.impact}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="event-timeline">
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            angle={-45}
            textAnchor="end"
            height={80}
            tick={{ fontSize: 12 }}
          />
          <YAxis
            type="number"
            domain={[-0.5, 3.5]}
            ticks={[0, 1, 2, 3]}
            tickFormatter={(value) => {
              const labels = ["Other", "Economic", "Geopolitical", "OPEC"];
              return labels[value] || "";
            }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Scatter name="Events" data={scatterData}>
            {scatterData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Scatter>
          {changepoint && changepoint.change_point_date && (
            <line
              x1={changepoint.change_point_date}
              x2={changepoint.change_point_date}
              y1={0}
              y2={1}
              stroke="red"
              strokeWidth={2}
              strokeDasharray="5 5"
            />
          )}
        </ScatterChart>
      </ResponsiveContainer>

      <div className="event-table">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Type</th>
              <th>Description</th>
              <th>Expected Impact</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event, idx) => (
              <tr key={idx} className={`event-type-${event.Event_Type}`}>
                <td>{event.Date}</td>
                <td>
                  <span className={`event-badge ${event.Event_Type}`}>
                    {event.Event_Type.replace("_", " ")}
                  </span>
                </td>
                <td>{event.Description}</td>
                <td>{event.Expected_Impact}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default EventTimeline;
