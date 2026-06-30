import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import Navigation from './components/Navigation'
import Sidebar from './components/Sidebar'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Scans from './pages/Scans'
import Results from './pages/Results'
import Reports from './pages/Reports'
import './App.css'

function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-gradient-to-br from-primary-900 via-slate-900 to-slate-800">
        <Sidebar />
        <main className="flex-1 flex flex-col">
          <Navigation />
          <div className="flex-1 overflow-auto">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/scans" element={<Scans />} />
              <Route path="/scans/:scanId" element={<Results />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  )
}

export default App