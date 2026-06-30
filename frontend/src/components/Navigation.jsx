import { motion } from 'framer-motion'
import { FiBell, FiUser, FiLogOut } from 'react-icons/fi'

const Navigation = () => {
  return (
    <motion.nav
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-slate-950 border-b border-primary-700/50 px-6 py-4 flex items-center justify-between shadow-lg"
    >
      <div className="flex-1">
        <h2 className="text-xl font-bold text-white">AegisRecon Pro</h2>
      </div>

      <div className="flex items-center gap-4">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          className="p-2 hover:bg-slate-800 rounded-lg text-slate-300 hover:text-primary-400 transition-colors"
        >
          <FiBell className="text-xl" />
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          className="p-2 hover:bg-slate-800 rounded-lg text-slate-300 hover:text-primary-400 transition-colors"
        >
          <FiUser className="text-xl" />
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          className="p-2 hover:bg-red-900/50 rounded-lg text-slate-300 hover:text-danger-400 transition-colors"
        >
          <FiLogOut className="text-xl" />
        </motion.button>
      </div>
    </motion.nav>
  )
}

export default Navigation