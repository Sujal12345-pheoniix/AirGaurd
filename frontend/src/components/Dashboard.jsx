import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Wind, Droplets, Thermometer, Activity, MapPin } from 'lucide-react'

const Dashboard = () => {
    const [aqiData, setAqiData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [useLocation, setUseLocation] = useState(false)
    const [locationError, setLocationError] = useState(null)

    const [formData, setFormData] = useState({
        pm25: 45,
        pm10: 80,
        no2: 20,
        so2: 15,
        o3: 30,
        co: 0.5,
        temperature: 25,
        humidity: 60,
        wind_speed: 10
    })

    // Manual prediction (ML Model)
    const predictAQI = async () => {
        setLoading(true)
        try {
            const response = await axios.post('http://localhost:8000/api/predict-aqi', formData)
            setAqiData(response.data)
            setUseLocation(false)
        } catch (error) {
            console.error("Error fetching AQI:", error)
            alert("Failed to connect to backend. Please ensure the backend server is running on port 8000.")
        }
        setLoading(false)
    }

    // Location-based prediction (Open-Meteo)
    const fetchLocationAQI = () => {
        if (!navigator.geolocation) {
            setLocationError("Geolocation is not supported by your browser.")
            return
        }

        setLoading(true)
        setLocationError(null)

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                try {
                    const { latitude, longitude } = position.coords
                    const response = await axios.post('http://localhost:8000/api/location-aqi', {
                        latitude,
                        longitude
                    })
                    setAqiData(response.data)
                    setUseLocation(true)

                    // Update inputs to show fetched components if available
                    if (response.data.components) {
                        const c = response.data.components
                        setFormData(prev => ({
                            ...prev,
                            pm25: c.pm25 || prev.pm25,
                            pm10: c.pm10 || prev.pm10,
                            no2: c.no2 || prev.no2,
                            so2: c.so2 || prev.so2,
                            o3: c.o3 || prev.o3,
                            co: c.co || prev.co,
                        }))
                    }
                } catch (error) {
                    console.error("Error fetching location AQI:", error)
                    if (error.message === 'Network Error') {
                        setLocationError("Cannot connect to Backend. Is the server running on port 8000?")
                    } else {
                        setLocationError("Failed to fetch data for your location.")
                    }
                }
                setLoading(false)
            },
            (error) => {
                setLoading(false)
                setLocationError("Unable to retrieve your location.")
            }
        )
    }

    useEffect(() => {
        // Initial load: Try location first, else manual default
        // fetchLocationAQI() // Optional: auto-fetch on load
        predictAQI()
    }, [])

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: parseFloat(e.target.value)
        })
    }

    return (
        <div className="dashboard">
            <h1>AirGuard <span style={{ color: 'var(--accent)' }}>AI</span></h1>
            <p>Real-time AQI Prediction & Health Advisory</p>

            {/* Buttons */}
            <div style={{ marginBottom: '20px' }}>
                <button onClick={predictAQI} style={{ marginRight: '10px', background: !useLocation ? 'var(--accent)' : '#333', color: !useLocation ? '#000' : '#fff' }}>
                    Manual Input
                </button>
                <button onClick={fetchLocationAQI} style={{ background: useLocation ? 'var(--accent)' : '#333', color: useLocation ? '#000' : '#fff' }}>
                    <MapPin size={16} style={{ marginRight: '5px', verticalAlign: 'text-bottom' }} />
                    Use My Location
                </button>
            </div>

            {locationError && <p style={{ color: 'red' }}>{locationError}</p>}

            <div className="card">
                <h2>{useLocation ? "Live Location AQI" : "Predicted AQI"}</h2>
                {loading ? <p>Analyzing...</p> : (
                    <div style={{ color: aqiData?.color || '#fff' }}>
                        <div className="aqi-display">{aqiData?.aqi ? Math.round(aqiData.aqi) : '--'}</div>
                        <h3>{aqiData?.category || 'Unknown'}</h3>
                    </div>
                )}
            </div>

            <div className="grid">
                <div className="card">
                    <h3>Health Advice</h3>
                    <ul style={{ textAlign: 'left', listStyle: 'none', padding: 0 }}>
                        <li style={{ marginBottom: '10px' }}><strong>General:</strong> {aqiData?.advice?.general}</li>
                        <li style={{ marginBottom: '10px' }}><strong>Mask:</strong> {aqiData?.advice?.mask}</li>
                        <li style={{ marginBottom: '10px' }}><strong>Activity:</strong> {aqiData?.advice?.outdoor_activity}</li>
                    </ul>
                </div>

                <div className="card">
                    <h3>Parameters {useLocation && "(Live Data)"}</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', textAlign: 'left' }}>

                        <label>PM2.5: <input type="number" name="pm25" value={formData.pm25} onChange={handleChange} disabled={useLocation} style={{ width: '60px' }} /></label>
                        <label>PM10: <input type="number" name="pm10" value={formData.pm10} onChange={handleChange} disabled={useLocation} style={{ width: '60px' }} /></label>
                        <label>NO2: <input type="number" name="no2" value={formData.no2} onChange={handleChange} disabled={useLocation} style={{ width: '60px' }} /></label>
                        <label>SO2: <input type="number" name="so2" value={formData.so2} onChange={handleChange} disabled={useLocation} style={{ width: '60px' }} /></label>
                        <label>O3: <input type="number" name="o3" value={formData.o3} onChange={handleChange} disabled={useLocation} style={{ width: '60px' }} /></label>
                        <label>CO: <input type="number" name="co" value={formData.co} onChange={handleChange} disabled={useLocation} style={{ width: '60px' }} /></label>

                    </div>
                    {!useLocation && <button onClick={predictAQI} style={{ marginTop: '20px', width: '100%' }}>Recalculate</button>}
                </div>
            </div>
        </div>
    )
}

export default Dashboard
