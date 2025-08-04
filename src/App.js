// src/App.js
import React, { useEffect, useState } from 'react';
import Papa from 'papaparse';
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts';

function App() {
  // State holds both pie-chart data and histogram data
  const [chartData, setChartData] = useState({
    pieData: [],
    histogramData: []
  });

  useEffect(() => {
    // Fetch & parse the CSV located at public/data/used_cars.csv
    Papa.parse('/data/used_cars.csv', {
      header: true,
      download: true,
      dynamicTyping: true,
      complete: ({ data }) => {
        // ─────────────── Pie Chart Data ───────────────
        // Count number of cars per body_type
        const counts = {};
        data.forEach(row => {
          if (row.body_type) {
            counts[row.body_type] = (counts[row.body_type] || 0) + 1;
          }
        });
        const pieData = Object.entries(counts).map(
          ([name, value]) => ({ name, value })
        );

        // ────────────── Histogram Data ──────────────
        // Extract all numeric prices
        const prices = data
          .map(r => r.Price_USD)
          .filter(v => typeof v === 'number' && !isNaN(v));

        // Define bin size and calculate number of bins
        const binSize = 5000;
        const maxPrice = Math.max(...prices);
        const numBins = Math.ceil(maxPrice / binSize);

        // Tally counts in each bin
        const histCounts = Array(numBins).fill(0);
        prices.forEach(price => {
          const idx = Math.min(Math.floor(price / binSize), numBins - 1);
          histCounts[idx]++;
        });

        // Convert counts into [{ range, count }] format
        const histogramData = histCounts.map((count, i) => ({
          range: `$${i * binSize}–${(i + 1) * binSize}`,
          count
        }));

        // Update state with both datasets
        setChartData({ pieData, histogramData });
      }
    });
  }, []);

  // Color palette for pie slices
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div style={{ padding: 20 }}>
      <h1 style={{ textAlign: 'center' }}>Used Car Sales Dashboard</h1>

      {/* Pie Chart: Cars by Body Type */}
      <div style={{ width: '100%', height: 400, marginBottom: 50 }}>
        <h2 style={{ textAlign: 'center' }}>Cars by Body Type</h2>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={chartData.pieData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label
            >
              {chartData.pieData.map((entry, idx) => (
                <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Histogram: Price Distribution */}
      <div style={{ width: '100%', height: 400 }}>
        <h2 style={{ textAlign: 'center' }}>Price Distribution (USD)</h2>
        <ResponsiveContainer>
          <BarChart
            data={chartData.histogramData}
            margin={{ top: 20, right: 30, bottom: 60, left: 20 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="range"
              angle={-45}
              textAnchor="end"
              interval={0}
              height={60}
            />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;
