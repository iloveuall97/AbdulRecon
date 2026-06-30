import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { FiShield, FiActivity, FiBarChart3, FiFileText, FiSettings } from 'react-icons/fi'

const menuItems = [
  { path: '/', icon: FiActivity, label: 'Home' },
  { path: '/dashboard', icon: FiBarChart3, label: 'Dashboard' },
  { path: '/scans', icon: FiShield, label: 'Scans' },
  { path: '/reports', icon: FiFileText, label: 'Reports' },
  { path: '/settings', icon: FiSettings, label: 'Settings' },
]

const Sidebar = () => {
  const location = useLocation()

  return (
    <motion.aside
      initial={{ x: -250 }}
      animate={{ x: 0 }}
      className="hidden md:flex flex-col w-64 bg-slate-950 border-r border-primary-700/50 shadow-lg"
    >
      <div className="p-6 border-b border-primary-700/50">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="flex items-center gap-3"
        >
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
            <FiShield className="text-white text-xl" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white">AegisRecon</h1>
            <p className="text-xs text-primary-400">Pro v1.0.0</p>
          </div>
        </motion.div>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item, index) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path

          return (
            <Link key={item.path} to={item.path}>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`px-4 py-3 rounded-lg flex items-center gap-3 transition-all ${
                  isActive
                    ? 'bg-primary-600 text-white shadow-lg'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-primary-400'
                }`}
              >
                <Icon className="text-lg" />
                <span className="font-medium">{item.label}</span>
              </motion.div>
            </Link>
          )
        })}
      </nav>

      <div className="p-4 border-t border-primary-700/50">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="bg-primary-900/50 rounded-lg p-3 border border-primary-700/50"
        >
          <p className="text-xs text-primary-300 text-center">
            <span className="font-bold">Authorized Testing Only</span>
            <br />
            Use responsibly
          </p>
        </motion.div>
      </div>
    </motion.aside>
  )
}

export default Sidebar