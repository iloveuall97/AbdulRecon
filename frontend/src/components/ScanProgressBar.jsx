import { motion } from 'framer-motion'
import { FiCheck, FiX, FiClock } from 'react-icons/fi'

const ScanProgressBar = ({ progress, status }) => {
  const getStatusColor = () => {
    switch (status) {
      case 'running':
        return 'bg-primary-500'
      case 'completed':
        return 'bg-success-500'
      case 'failed':
        return 'bg-danger-500'
      default:
        return 'bg-slate-500'
    }
  }

  const getStatusIcon = () => {
    switch (status) {
      case 'running':
        return <FiClock className="animate-spin" />
      case 'completed':
        return <FiCheck />
      case 'failed':
        return <FiX />
      default:
        return null
    }
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-300">Progress</span>
        <div className="flex items-center gap-2">
          <span className="text-sm text-slate-400">{progress}%</span>
          <motion.div
            initial={{ rotate: 0 }}
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity }}
            className="text-primary-400"
          >
            {getStatusIcon()}
          </motion.div>
        </div>
      </div>
      <div className="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.5 }}
          className={`h-full ${getStatusColor()} rounded-full`}
        />
      </div>
    </div>
  )
}

export default ScanProgressBar