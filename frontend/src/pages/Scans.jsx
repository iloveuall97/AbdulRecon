import { motion } from 'framer-motion'
import { useState } from 'react'
import { FiPlay, FiPlus } from 'react-icons/fi'
import ScanProgressBar from '../components/ScanProgressBar'

const Scans = () => {
  const [scans] = useState([
    { id: 1, target: 'example.com', status: 'completed', progress: 100, date: '2024-01-15' },
    { id: 2, target: 'api.example.com', status: 'running', progress: 65, date: '2024-01-15' },
    { id: 3, target: 'test.example.com', status: 'pending', progress: 0, date: '2024-01-14' },
  ])

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Scans</h1>
          <p className="text-slate-400">Manage and monitor security scans</p>
        </div>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-500 hover:to-primary-600 text-white font-bold py-2 px-4 rounded-lg inline-flex items-center gap-2 transition-all"
        >
          <FiPlus className="text-lg" />
          New Scan
        </motion.button>
      </motion.div>

      {/* Scans List */}
      <div className="space-y-4">
        {scans.map((scan, index) => (
          <motion.div
            key={scan.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -2 }}
            className="bg-slate-800 border border-primary-600/30 rounded-xl p-6 backdrop-blur-sm hover:border-primary-500/50 transition-all"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-bold text-white">{scan.target}</h3>
                <p className="text-sm text-slate-400">{scan.date}</p>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                scan.status === 'completed'
                  ? 'bg-success-500/20 text-success-400'
                  : scan.status === 'running'
                  ? 'bg-primary-500/20 text-primary-400'
                  : 'bg-slate-600/50 text-slate-300'
              }`}>
                {scan.status.charAt(0).toUpperCase() + scan.status.slice(1)}
              </span>
            </div>
            <ScanProgressBar progress={scan.progress} status={scan.status} />
          </motion.div>
        ))}
      </div>
    </div>
  )
}

export default Scans