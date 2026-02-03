import React, { useState } from 'react'
import Dashboard from './components/Dashboard'
import Chatbot from './components/Chatbot'

function App() {
    return (
        <div className="app-container">
            <Dashboard />
            <Chatbot />
        </div>
    )
}

export default App
