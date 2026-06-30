import { motion } from 'framer-motion'
import { FiArrowRight, FiShield, FiRapidFire } from 'react-icons/fi'
import { Link } from 'react-router-dom'

const Home = () => {
  const features = [
    {
      icon: FiShield,
      title: 'Advanced Detection',
      description: 'Multi-vector vulnerability detection with advanced techniques',
    },
    {
      icon: FiRapidFire,
      title: 'Fast Scanning',
      description: 'Concurrent asynchronous scanning for maximum performance',
    },
    {
      icon: FiShield,
      title: 'Professional Reports',
      description: 'Generate comprehensive security assessment reports',
    },
  ]

  return (
    <div className="flex-1 overflow-auto">
      <div className="min-h-full bg-gradient-to-b from-transparent to-slate-900/50">
        {/* Hero Section */}
        <motion.section
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="px-6 py-20 text-center"
        >
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="max-w-4xl mx-auto"
          >
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
              AegisRecon Pro
            </h1>
            <p className="text-xl text-slate-300 mb-8">
              Professional Security Testing & Vulnerability Assessment Platform
            </p>
            <Link to="/scans">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-500 hover:to-primary-600 text-white font-bold py-3 px-8 rounded-lg inline-flex items-center gap-2 transition-all shadow-lg"
              >
                Start New Scan
                <FiArrowRight className="text-lg" />
              </motion.button>
            </Link>
          </motion.div>
        </motion.section>

        {/* Features Section */}
        <section className="px-6 py-20 max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-3xl font-bold text-white mb-12 text-center"
          >
            Powerful Features
          </motion.h2>
          <div className="grid md:grid-cols-3 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 + index * 0.1 }}
                  whileHover={{ y: -10 }}
                  className="bg-slate-800/50 border border-primary-600/30 rounded-xl p-6 backdrop-blur-sm hover:border-primary-500/50 transition-all"
                >
                  <div className="text-4xl text-primary-400 mb-4">
                    <Icon />
                  </div>
                  <h3 className="text-lg font-bold text-white mb-2">{feature.title}</h3>
                  <p className="text-slate-400 text-sm">{feature.description}</p>
                </motion.div>
              )
            })}
          </div>
        </section>
      </div>
    </div>
  )
}

export default Home