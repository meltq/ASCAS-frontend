import React, { useState } from 'react';
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

function App_new() {
  const [sat1Id, setSat1Id] = useState('');
  const [sat2Id, setSat2Id] = useState('');
  const [positions, setPositions] = useState({
    sat1: { current: null, future: [], orbitalEquation: null },
    sat2: { current: null, future: [], orbitalEquation: null }
  });
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [selectedSatellite, setSelectedSatellite] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [alternativeOrbits, setAlternativeOrbits] = useState({
    sat1: null,
    sat2: null,
  });
  const [transferEnergy, setTransferEnergy] = useState({
    sat1: null,
    sat2: null,
  });
  const [optimalTransferEnergy, setOptimalTransferEnergy] = useState({
    sat1: null,
    sat2: null,
  });
  const [riskFactor, setRiskFactor] = useState({
    sat1: null,
    sat2: null,
  });

  // Function to generate random values
  const generateRandomValues = () => {
    const randomOrbit = () => ({
      radius: (Math.random() * 10000 + 42000).toFixed(2), // random radius between 42000 and 52000 km
      equation: `(x / ${(Math.random() * 10000 + 42165).toFixed(2)})^2 + (y / ${(Math.random() * 10000 + 42165).toFixed(2)})^2 = 1`,
    });

    setAlternativeOrbits({
      sat1: randomOrbit(),
      sat2: randomOrbit(),
    });

    setTransferEnergy({
      sat1: (Math.random() * 100).toFixed(2), // random transfer energy in arbitrary units
      sat2: (Math.random() * 100).toFixed(2),
    });

    setOptimalTransferEnergy({
      sat1: (Math.random() * 500).toFixed(2), // random optimal transfer energy in arbitrary units
      sat2: (Math.random() * 500).toFixed(2),
    });
    // Set random risk factors
    setRiskFactor({
        sat1: (Math.random() * 10).toFixed(2), // random risk factor in percentage
        sat2: (Math.random() * 10).toFixed(2),
      });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null); // Reset error state
    try {
      const response = await fetch('http://127.0.0.1:5000/api/positions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sat1Id, sat2Id }),
      });
      const data = await response.json();
      if (response.ok) {
        // Set current positions, future positions, and orbital equations
        setPositions({
          sat1: {
            current: data.currentPositionSat1,
            future: data.futurePositionsSat1,
            orbitalEquation: data.orbitalEquationSat1
          },
          sat2: {
            current: data.currentPositionSat2,
            future: data.futurePositionsSat2,
            orbitalEquation: data.orbitalEquationSat2
          }
        });
        
        // Generate random values
        generateRandomValues();
      } else {
        throw new Error(data.error || 'Failed to fetch positions');
      }
    } catch (error) {
      setError(error.message); // Set error state
      console.error('Error fetching positions:', error);
    } finally {
      setLoading(false); // Stop loading state
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
      <header className="text-center p-6 bg-gray-900 bg-opacity-80">
        <h1 className="text-4xl text-white font-bold">ASCAS</h1>
        <p className="mt-2 text-lg text-gray-300">Monitor and maneuvers the positions of satellites to prevent collisions.</p>
      </header>

      <div className="flex items-center justify-center min-h-screen">
        <div className="flex flex-col items-center justify-center mt-10 mx-4 p-6 bg-opacity-80 bg-gray-900 rounded-lg shadow-lg w-full max-w-3xl">
          <form onSubmit={handleSubmit} className="space-y-6 w-full">
            <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 justify-between">
              {/* Dropdown for First Satellite */}
              <div className="w-full md:w-1/2">
                <label className="block text-lg font-medium mb-2 text-white">Select First Satellite:</label>
                <select
                  className="px-4 py-2 w-full border border-gray-300 rounded-lg focus:outline-none text-black"
                  value={sat1Id}
                  onChange={(e) => setSat1Id(e.target.value)}
                >
                  <option value="">-- Select Satellite --</option>
                  {satelliteList.map((satellite) => (
                    <option key={satellite.norad_id} value={satellite.norad_id}>
                      {satellite.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Dropdown for Second Satellite */}
              <div className="w-full md:w-1/2">
                <label className="block text-lg font-medium mb-2 text-white">Select Second Satellite:</label>
                <select
                  className="px-4 py-2 w-full border border-gray-300 rounded-lg focus:outline-none text-black"
                  value={sat2Id}
                  onChange={(e) => setSat2Id(e.target.value)}
                >
                  <option value="">-- Select Satellite --</option>
                  {satelliteList.map((satellite) => (
                    <option key={satellite.norad_id} value={satellite.norad_id}>
                      {satellite.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <button
              type="submit"
              className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition"
              disabled={loading} // Disable button while loading
            >
              {loading ? 'Fetching...' : 'Fetch Positions'}
            </button>
          </form>

          {/* Display Error Message */}
          {error && <p className="text-red-500 mt-4">{error}</p>}

          {/* Display Current and Future Positions */}
          {positions.sat1.current && positions.sat2.current && (
            <div className="mt-8 text-white flex flex-col md:flex-row justify-between w-full">
              {/* Satellite 1 Details */}
              <div className="border border-blue-600 p-6 rounded-lg bg-gray-800 shadow-lg w-full md:w-1/2 m-2">
                <h3 className="text-3xl font-bold">Satellite 1 ({sat1Id})</h3>
                <p className="mt-4">Current Position:</p>
                <div className="flex flex-col">
                  <span className="font-semibold">X: {positions.sat1.current.x.toFixed(2)}</span>
                  <span className="font-semibold">Y: {positions.sat1.current.y.toFixed(2)}</span>
                  <span className="font-semibold">Z: {positions.sat1.current.z.toFixed(2)}</span>
                </div>
                <p className="mt-4">Future Positions:</p>
                {positions.sat1.future.map((pos, index) => (
                  <div key={index} className="flex flex-col">
                    <span>X: {pos.x.toFixed(2)}, Y: {pos.y.toFixed(2)}, Z: {pos.z.toFixed(2)}</span>
                  </div>
                ))}
                <button
                  onClick={() => handleSatelliteClick(satelliteList.find(sat => sat.norad_id == sat1Id))}
                  className="bg-blue-600 text-white py-2 px-4 mt-4 rounded-lg hover:bg-blue-700 transition"
                >
                  More Info
                </button>
              </div>

              {/* Satellite 2 Details */}
              <div className="border border-blue-600 p-6 rounded-lg bg-gray-800 shadow-lg w-full md:w-1/2 m-2">
                <h3 className="text-3xl font-bold">Satellite 2 ({sat2Id})</h3>
                <p className="mt-4">Current Position:</p>
                <div className="flex flex-col">
                  <span className="font-semibold">X: {positions.sat2.current.x.toFixed(2)}</span>
                  <span className="font-semibold">Y: {positions.sat2.current.y.toFixed(2)}</span>
                  <span className="font-semibold">Z: {positions.sat2.current.z.toFixed(2)}</span>
                </div>
                <p className="mt-4">Future Positions:</p>
                {positions.sat2.future.map((pos, index) => (
                  <div key={index} className="flex flex-col">
                    <span>X: {pos.x.toFixed(2)}, Y: {pos.y.toFixed(2)}, Z: {pos.z.toFixed(2)}</span>
                  </div>
                ))}
                <button
                  onClick={() => handleSatelliteClick(satelliteList.find(sat => sat.norad_id == sat2Id))}
                  className="bg-blue-600 text-white py-2 px-4 mt-4 rounded-lg hover:bg-blue-700 transition"
                >
                  More Info
                </button>
              </div>
            </div>
          )}

          {/* Display Orbital Equations */}
          {positions.sat1.orbitalEquation && positions.sat2.orbitalEquation && (
            <div className="mt-8 text-white">
              <h3 className="text-2xl font-bold">Orbital Equations:</h3>
              <div className="flex flex-col md:flex-row justify-between">
                <div className="border border-blue-600 p-4 rounded-lg bg-gray-800 shadow-lg w-full md:w-1/2 m-2">
                  <h4 className="font-semibold">Satellite 1 Equation:</h4>
                  <p>{positions.sat1.orbitalEquation}</p>
                </div>
                <div className="border border-blue-600 p-4 rounded-lg bg-gray-800 shadow-lg w-full md:w-1/2 m-2">
                  <h4 className="font-semibold">Satellite 2 Equation:</h4>
                  <p>{positions.sat2.orbitalEquation}</p>
                </div>
              </div>
            </div>
          )}

          {/* Display Alternative Orbits and Transfer Energies */}
          {alternativeOrbits.sat1 && alternativeOrbits.sat2 && (
            <div className="mt-8 text-white">
              <h3 className="text-2xl font-bold">Alternative Orbits:</h3>
              <div className="flex flex-col md:flex-row justify-between">
                <div className="border border-blue-600 p-4 rounded-lg bg-gray-800 shadow-lg w-full md:w-1/2 m-2">
                  <h4 className="font-semibold">Satellite 1 Alternative Orbit:</h4>
                  <p>Radius: {alternativeOrbits.sat1.radius} km</p>
                  <p>Equation: {alternativeOrbits.sat1.equation}</p>
                  <p>Transfer Energy: {transferEnergy.sat1} units</p>
                  <p>Optimal Transfer Energy: {optimalTransferEnergy.sat1} units</p>
                  <p>Risk Factor: {riskFactor.sat1}</p>
                </div>
                <div className="border border-blue-600 p-4 rounded-lg bg-gray-800 shadow-lg w-full md:w-1/2 m-2">
                  <h4 className="font-semibold">Satellite 2 Alternative Orbit:</h4>
                  <p>Radius: {alternativeOrbits.sat2.radius} km</p>
                  <p>Equation: {alternativeOrbits.sat2.equation}</p>
                  <p>Transfer Energy: {transferEnergy.sat2} units</p>
                  <p>Optimal Transfer Energy: {optimalTransferEnergy.sat2} units</p>
                  <p>Risk Factor: {riskFactor.sat2}</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Modal for Satellite Information */}
        <Modal
          isOpen={modalIsOpen}
          onRequestClose={closeModal}
          className="bg-gray-800 p-6 rounded-lg max-w-md mx-auto mt-20"
          overlayClassName="fixed inset-0 bg-black bg-opacity-70"
        >
          <h2 className="text-2xl font-bold text-white mb-4">Satellite Information</h2>
          {selectedSatellite && (
            <div>
              <p className="text-white">Name: {selectedSatellite.name}</p>
              <p className="text-white">NORAD ID: {selectedSatellite.norad_id}</p>
            </div>
          )}
          <button
            onClick={closeModal}
            className="bg-red-600 text-white py-2 px-4 rounded-lg mt-4 hover:bg-red-700 transition"
          >
            Close
          </button>
        </Modal>
      </div>

      <footer className="p-4 text-center bg-gray-900 text-white">
        <p>&copy; {new Date().getFullYear()} ASCAS. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App_new;
