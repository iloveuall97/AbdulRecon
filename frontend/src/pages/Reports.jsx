import { motion } from 'framer-motion'
import { FiDownload, FiFileText } from 'react-icons/fi'

const Reports = () => {
  const reports = [
    { id: 1, name: 'example.com - Q4 2023', date: '2024-01-15', size: '2.4 MB' },
    { id: 2, name: 'api.example.com - Jan 2024', date: '2024-01-12', size: '1.8 MB' },
    { id: 3, name: 'test.example.com - Jan 2024', date: '2024-01-10', size: '3.2 MB' },
  ]

  return (
    <div className="p-6 space-y-6">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold text-white mb-2">Reports</h1>
        <p className="text-slate-400">Download and manage security assessment reports</p>
      </motion.div>

      <div className="grid gap-4">
        {reports.map((report, index) => (
          <motion.div
            key={report.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-slate-800 border border-primary-600/30 rounded-xl p-6 backdrop-blur-sm hover:border-primary-500/50 transition-all flex items-center justify-between"
          >
            <div className="flex items-center gap-4">
              <div className="p-3 bg-primary-500/20 rounded-lg">
                <FiFileText className="text-2xl text-primary-400" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">{report.name}</h3>
                <p className="text-sm text-slate-400">{report.date} • {report.size}</p>
              </div>
            </div>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 hover:bg-slate-700 rounded-lg text-primary-400 hover:text-primary-300 transition-colors"
            >
              <FiDownload className="text-xl" />
            </motion.button>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

export default Reports