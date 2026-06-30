import { motion } from 'framer-motion'
import { useParams } from 'react-router-dom'

const Results = () => {
  const { scanId } = useParams()

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-6 space-y-6"
    >
      <h1 className="text-3xl font-bold text-white mb-2">Scan Results</h1>
      <p className="text-slate-400">Scan ID: {scanId}</p>
      <div className="bg-slate-800 border border-primary-600/30 rounded-xl p-6 backdrop-blur-sm text-white text-center py-20">
        <p className="text-slate-400">Results will be displayed here</p>
      </div>
    </motion.div>
  )
}

export default Results