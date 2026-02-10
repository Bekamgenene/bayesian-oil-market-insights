import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const DateFilter = ({ dateRange, filters, onFilterChange }) => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [selectedEventTypes, setSelectedEventTypes] = useState([]);

  const eventTypes = ["OPEC_Decision", "Geopolitical", "Economic_Shock"];

  useEffect(() => {
    if (filters.startDate) {
      setStartDate(new Date(filters.startDate));
    }
    if (filters.endDate) {
      setEndDate(new Date(filters.endDate));
    }
    if (filters.eventTypes) {
      setSelectedEventTypes(filters.eventTypes);
    }
  }, [filters]);

  const handleStartDateChange = (date) => {
    setStartDate(date);
    const dateStr = date ? date.toISOString().split("T")[0] : null;
    onFilterChange({
      ...filters,
      startDate: dateStr,
    });
  };

  const handleEndDateChange = (date) => {
    setEndDate(date);
    const dateStr = date ? date.toISOString().split("T")[0] : null;
    onFilterChange({
      ...filters,
      endDate: dateStr,
    });
  };

  const handleEventTypeToggle = (eventType) => {
    const newEventTypes = selectedEventTypes.includes(eventType)
      ? selectedEventTypes.filter((t) => t !== eventType)
      : [...selectedEventTypes, eventType];

    setSelectedEventTypes(newEventTypes);
    onFilterChange({
      ...filters,
      eventTypes: newEventTypes,
    });
  };

  const handleReset = () => {
    setStartDate(null);
    setEndDate(null);
    setSelectedEventTypes([]);
    onFilterChange({
      startDate: null,
      endDate: null,
      eventTypes: [],
    });
  };

  const minDate = dateRange.min ? new Date(dateRange.min) : null;
  const maxDate = dateRange.max ? new Date(dateRange.max) : null;

  return (
    <div className="date-filter">
      <h3>Filters</h3>

      <div className="filter-section">
        <label>Start Date</label>
        <DatePicker
          selected={startDate}
          onChange={handleStartDateChange}
          selectsStart
          startDate={startDate}
          endDate={endDate}
          minDate={minDate}
          maxDate={maxDate}
          dateFormat="yyyy-MM-dd"
          placeholderText="Select start date"
          isClearable
        />
      </div>

      <div className="filter-section">
        <label>End Date</label>
        <DatePicker
          selected={endDate}
          onChange={handleEndDateChange}
          selectsEnd
          startDate={startDate}
          endDate={endDate}
          minDate={startDate || minDate}
          maxDate={maxDate}
          dateFormat="yyyy-MM-dd"
          placeholderText="Select end date"
          isClearable
        />
      </div>

      <div className="filter-section">
        <label>Event Types</label>
        <div className="event-type-checkboxes">
          {eventTypes.map((eventType) => (
            <div key={eventType} className="checkbox-item">
              <input
                type="checkbox"
                id={`event-${eventType}`}
                checked={selectedEventTypes.includes(eventType)}
                onChange={() => handleEventTypeToggle(eventType)}
              />
              <label htmlFor={`event-${eventType}`}>
                {eventType.replace("_", " ")}
              </label>
            </div>
          ))}
        </div>
      </div>

      <button className="reset-button" onClick={handleReset}>
        Reset Filters
      </button>

      <div className="filter-info">
        <p>
          {startDate || endDate || selectedEventTypes.length > 0
            ? `Active filters: ${[
                startDate && "Start date",
                endDate && "End date",
                selectedEventTypes.length > 0 &&
                  `${selectedEventTypes.length} event types`,
              ]
                .filter(Boolean)
                .join(", ")}`
            : "No filters applied"}
        </p>
      </div>
    </div>
  );
};

export default DateFilter;
