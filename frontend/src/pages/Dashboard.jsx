import { motion } from 'framer-motion'
import StatCard from '../components/StatCard'
import VulnerabilityHeatmap from '../components/VulnerabilityHeatmap'
import ScanHistory from '../components/ScanHistory'
import { FiAlertTriangle, FiCheckCircle, FiClock, FiTrendingUp } from 'react-icons/fi'

const Dashboard = () => {
  const vulnerabilityData = [
    { name: 'critical', value: 5 },
    { name: 'high', value: 12 },
    { name: 'medium', value: 28 },
    { name: 'low', value: 45 },
    { name: 'info', value: 67 },
  ]

  const scanHistoryData = [
    { date: 'Mon', vulnerabilities: 5 },
    { date: 'Tue', vulnerabilities: 8 },
    { date: 'Wed', vulnerabilities: 3 },
    { date: 'Thu', vulnerabilities: 12 },
    { date: 'Fri', vulnerabilities: 7 },
    { date: 'Sat', vulnerabilities: 9 },
    { date: 'Sun', vulnerabilities: 4 },
  ]

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-slate-400">Real-time security scanning overview</p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-4 gap-4">
        <StatCard
          icon={FiAlertTriangle}
          label="Total Vulnerabilities"
          value="157"
          trend="+12 today"
          color="danger"
        />
        <StatCard
          icon={FiAlertTriangle}
          label="Critical Issues"
          value="5"
          trend="-1 from last week"
          color="danger"
        />
        <StatCard
          icon={FiCheckCircle}
          label="Scans Completed"
          value="42"
          trend="+8 this week"
          color="success"
        />
        <StatCard
          icon={FiClock}
          label="Avg Scan Time"
          value="3.2m"
          trend="-15%"
          color="primary"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        <VulnerabilityHeatmap data={vulnerabilityData} />
        <ScanHistory data={scanHistoryData} />
      </div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-slate-800 border border-primary-600/30 rounded-xl p-6 backdrop-blur-sm"
      >
        <h3 className="text-lg font-bold text-white mb-4">Recent Scans</h3>
        <div className="space-y-3">
          {[1, 2, 3].map((_, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-slate-700/50 rounded-lg p-4 hover:bg-slate-700 transition-all flex items-center justify-between"
            >
              <div>
                <p className="text-white font-medium">example{i + 1}.com</p>
                <p className="text-sm text-slate-400">Completed 2 hours ago</p>
              </div>
              <span className="text-success-400 text-sm font-medium">12 issues</span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  )
}

export default Dashboard