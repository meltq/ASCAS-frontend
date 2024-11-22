import React, { useState, useEffect } from 'react';
import './index.css';
import backgroundImage from './images/background.jpg'; // Import your image
import Modal from 'react-modal'; // Modal library
import './style.css';

// Sample satellite list with NORAD IDs
const satelliteList = [
  { name: 'ISS (International Space Station)', norad_id: 25544 },
  { name: 'Hubble Space Telescope', norad_id: 27663 },
  { name: 'COSMOS 2251 (Debris)', norad_id: 22675 },
  { name: 'Iridium 33 (Debris)', norad_id: 24946 },
  { name: 'NOAA 19', norad_id: 33591 },
  { name: 'GOES 16', norad_id: 41866 },
  { name: 'Envisat', norad_id: 27386 },
  { name: 'Terra', norad_id: 25994 },
  { name: 'Sentinel-1A', norad_id: 39634 },
  { name: 'Sentinel-2A', norad_id: 40697 },
  { name: 'GPS IIR-10', norad_id: 25933 },
  { name: 'Landsat 8', norad_id: 39084 },
  { name: 'SES-10', norad_id: 42432 },
  { name: 'Aeolus', norad_id: 43600 },
];

Modal.setAppElement('#root'); // For accessibility

function App() {
  const [sat1Id, setSat1Id] = useState('');
  const [sat2Id, setSat2Id] = useState('');
  const [positions, setPositions] = useState({ sat1: null, sat2: null });
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [selectedSatellite, setSelectedSatellite] = useState(null);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Fetch positions from your backend
      const response = await fetch('http://127.0.0.1:5000/api/positions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sat1Id, sat2Id }),
      });
      const data = await response.json();
      if (response.ok) {
        // Set current and future positions
        setPositions({
          sat1: {
            current: data.currentPositionSat1,
            future: data.futurePositionsSat1,
          },
          sat2: {
            current: data.currentPositionSat2,
            future: data.futurePositionsSat2,
          },
        });
      } else {
        console.error('Error fetching positions:', data.error);
      }
    } catch (error) {
      console.error('Error fetching positions:', error);
    }
  };

  // Handle satellite click
  const handleSatelliteClick = (satellite) => {
    setSelectedSatellite(satellite);
    setModalIsOpen(true);
  };

  // Close the modal
  const closeModal = () => {
    setModalIsOpen(false);
    setSelectedSatellite(null);
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center"
      style={{ backgroundImage: `url(${backgroundImage})` }}
    >
      <div className="flex items-center justify-center min-h-screen">
        <div className="flex flex-col items-center justify-center mt-10 mx-4 p-6 bg-opacity-80 bg-gray-900 rounded-lg shadow-lg w-full max-w-3xl">
          <h2 className="text-5xl mb-8 font-mono text-white shadow-lg">Satellite Collision Avoidance</h2>

          <form onSubmit={handleSubmit} className="space-y-6 w-full">
            <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 justify-between">
              <div className="w-full md:w-1/2">
                <label className="block text-lg font-medium mb-2 text-white">First Satellite (NORAD ID):</label>
                <input
                  type="text"
                  className="px-4 py-2 w-full border border-gray-300 rounded-lg focus:outline-none text-black"
                  placeholder="e.g., 25544"
                  value={sat1Id}
                  onChange={(e) => setSat1Id(e.target.value)}
                />
              </div>
              <div className="w-full md:w-1/2">
                <label className="block text-lg font-medium mb-2 text-white">Second Satellite (NORAD ID):</label>
                <input
                  type="text"
                  className="px-4 py-2 w-full border border-gray-300 rounded-lg focus:outline-none text-black"
                  placeholder="e.g., 27663"
                  value={sat2Id}
                  onChange={(e) => setSat2Id(e.target.value)}
                />
              </div>
            </div>
            <button
              type="submit"
              className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition"
            >
              Fetch Positions
            </button>
          </form>

          {/* Display Current and Future Positions */}
          {/* Display Current and Future Positions */}
{positions.sat1 && positions.sat2 && (
  <div className="mt-8 text-white flex flex-col md:flex-row justify-between w-full">
    <div className="border border-blue-600 p-6 rounded-lg bg-gray-800 shadow-lg w-full md:w-1/2 m-2">
      <h3 className="text-3xl font-bold">Satellite 1 ({sat1Id})</h3>
      <p className="mt-4">Current Position:</p>
      <div className="flex flex-col">
        <span className="font-semibold">X: {positions.sat1.current.x}</span>
        <span className="font-semibold">Y: {positions.sat1.current.y}</span>
        <span className="font-semibold">Z: {positions.sat1.current.z}</span>
      </div>
      <h4 className="mt-4 font-semibold">Future Positions:</h4>
      <ul className="mt-2 space-y-1">
        {positions.sat1.future.map((pos, index) => (
          <li key={index} className="text-gray-400">
            <span className="font-semibold">In {index + 1} year(s):</span> 
            <div className="flex flex-col">
              <span>X: {pos.x}</span>
              <span>Y: {pos.y}</span>
              <span>Z: {pos.z}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
    <div className="border border-blue-600 p-6 rounded-lg bg-gray-800 shadow-lg w-full md:w-1/2 m-2">
      <h3 className="text-3xl font-bold">Satellite 2 ({sat2Id})</h3>
      <p className="mt-4">Current Position:</p>
      <div className="flex flex-col">
        <span className="font-semibold">X: {positions.sat2.current.x}</span>
        <span className="font-semibold">Y: {positions.sat2.current.y}</span>
        <span className="font-semibold">Z: {positions.sat2.current.z}</span>
      </div>
      <h4 className="mt-4 font-semibold">Future Positions:</h4>
      <ul className="mt-2 space-y-1">
        {positions.sat2.future.map((pos, index) => (
          <li key={index} className="text-gray-400">
            <span className="font-semibold">In {index + 1} year(s):</span>
            <div className="flex flex-col">
              <span>X: {pos.x}</span>
              <span>Y: {pos.y}</span>
              <span>Z: {pos.z}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  </div>
)}


          {/* Display Satellite List */}
          <div className="mt-8">
            <h3 className="text-3xl text-white">Available Satellites:</h3>
            <ul className="mt-4 space-y-4">
              {satelliteList.map((satellite) => (
                <li
                  key={satellite.norad_id}
                  onClick={() => handleSatelliteClick(satellite)}
                  className="cursor-pointer bg-gray-700 hover:bg-gray-600 transition p-4 rounded-lg shadow-md"
                >
                  <span className="text-blue-300 font-semibold">{satellite.name}</span> (NORAD ID: <span className="text-gray-400">{satellite.norad_id}</span>)
                </li>
              ))}
            </ul>
          </div>

          {/* Modal for Satellite Details */}
          <Modal isOpen={modalIsOpen} onRequestClose={closeModal}>
            <h2 className="text-2xl mb-4">{selectedSatellite ? selectedSatellite.name : ''}</h2>
            <button onClick={closeModal} className="text-blue-500 underline">Close</button>
          </Modal>
        </div>
      </div>
    </div>
  );
}

export default App;
