import { createCustomElement } from '/hacsfiles/custom-react-panel.js';
import React from 'react';
import { LineChart, XAxis, YAxis, CartesianGrid, Line, Tooltip, Legend } from 'recharts';
import { Flame, Thermometer, Wind, Bell } from 'lucide-react';

const HWAMDashboard = () => {
  const data = [
    {time: '12:00', stoveTemp: 480, roomTemp: 22, oxygen: 12},
    {time: '12:05', stoveTemp: 485, roomTemp: 22.5, oxygen: 11},
    {time: '12:10', stoveTemp: 490, roomTemp: 23, oxygen: 10},
  ];

  return (
    <div className="p-4 bg-white rounded-lg shadow-lg">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2">
          <Flame className="w-8 h-8 text-orange-500" />
          <h2 className="text-2xl font-bold">HWAM Poêle</h2>
        </div>
        <div className="flex space-x-4">
          <button className="px-4 py-2 text-white bg-orange-500 rounded hover:bg-orange-600">
            Mode Nuit
          </button>
          <button className="px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600">
            Paramètres
          </button>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="p-4 bg-gray-100 rounded flex items-center space-x-2">
          <Thermometer className="text-red-500" />
          <div>
            <div className="text-sm text-gray-500">Temp. Poêle</div>
            <div className="text-xl font-bold">{data[data.length-1].stoveTemp}°C</div>
          </div>
        </div>
        <div className="p-4 bg-gray-100 rounded flex items-center space-x-2">
          <Thermometer className="text-blue-500" />
          <div>
            <div className="text-sm text-gray-500">Temp. Pièce</div>
            <div className="text-xl font-bold">{data[data.length-1].roomTemp}°C</div>
          </div>
        </div>
        <div className="p-4 bg-gray-100 rounded flex items-center space-x-2">
          <Wind className="text-green-500" />
          <div>
            <div className="text-sm text-gray-500">Oxygène</div>
            <div className="text-xl font-bold">{data[data.length-1].oxygen}%</div>
          </div>
        </div>
        <div className="p-4 bg-gray-100 rounded flex items-center space-x-2">
          <Bell className="text-yellow-500" />
          <div>
            <div className="text-sm text-gray-500">État</div>
            <div className="text-xl font-bold">Normal</div>
          </div>
        </div>
      </div>

      <div className="w-full h-64">
        <LineChart 
          width={800} 
          height={250} 
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis 
            yAxisId="temp"
            domain={['auto', 'auto']}
            label={{ value: 'Température °C', angle: -90, position: 'insideLeft' }}
          />
          <YAxis 
            yAxisId="oxygen"
            orientation="right"
            domain={[0, 100]}
            label={{ value: 'Oxygène %', angle: 90, position: 'insideRight' }}
          />
          <Tooltip />
          <Legend />
          <Line yAxisId="temp" type="monotone" dataKey="stoveTemp" stroke="#ef4444" name="Temp. Poêle" />
          <Line yAxisId="temp" type="monotone" dataKey="roomTemp" stroke="#3b82f6" name="Temp. Pièce" />
          <Line yAxisId="oxygen" type="monotone" dataKey="oxygen" stroke="#22c55e" name="Oxygène" />
        </LineChart>
      </div>
    </div>
  );
};

createCustomElement("hwam-dashboard", HWAMDashboard);
