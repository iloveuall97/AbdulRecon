import { useState, useEffect } from 'react'
import axios from 'axios'

const useScanAPI = () => {
  const [scans, setScans] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchScans = async () => {
    setLoading(true)
    try {
      const response = await axios.get('/api/v1/scans')
      setScans(response.data.scans)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const createScan = async (target, scope, modules) => {
    setLoading(true)
    try {
      const response = await axios.post('/api/v1/scans', {
        target,
        scope,
        modules,
      })
      setError(null)
      return response.data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchScans()
  }, [])

  return {
    scans,
    loading,
    error,
    fetchScans,
    createScan,
  }
}

export default useScanAPI