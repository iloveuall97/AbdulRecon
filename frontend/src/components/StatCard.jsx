import { motion } from 'framer-motion'
import { FiTrendingUp, FiAlertTriangle, FiCheckCircle, FiClock } from 'react-icons/fi'

const StatCard = ({ icon: Icon, label, value, trend, color }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -5, boxShadow: '0 20px 25px -5rgba(0, 0, 0, 0.5)' }}
      className={`bg-slate-800 border border-${color}-600/30 rounded-xl p-6 backdrop-blur-sm hover:border-${color}-500/50 transition-all cursor-pointer`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-slate-400 text-sm font-medium">{label}</p>
          <p className="text-3xl font-bold text-white mt-2">{value}</p>
          {trend && (
            <div className="flex items-center gap-1 mt-2 text-green-400 text-sm">
              <FiTrendingUp className="text-lg" />
              <span>{trend}</span>
            </div>
          )}
        </div>
        <div className={`p-3 bg-${color}-500/20 rounded-lg`}>
          <Icon className={`text-2xl text-${color}-400`} />
        </div>
      </div>
    </motion.div>
  )
}

export default StatCard