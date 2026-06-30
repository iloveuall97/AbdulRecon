import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'

const useWebSocket = (url) => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const connect = () => {
      try {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const ws = new WebSocket(`${protocol}//${window.location.host}${url}`)

        ws.onopen = () => {
          setLoading(false)
        }

        ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data)
            setData(message)
          } catch (e) {
            console.error('WebSocket parse error:', e)
          }
        }

        ws.onerror = (event) => {
          setError('WebSocket connection error')
          console.error('WebSocket error:', event)
        }

        ws.onclose = () => {
          // Reconnect after 3 seconds
          setTimeout(connect, 3000)
        }

        return () => {
          ws.close()
        }
      } catch (e) {
        setError(e.message)
      }
    }

    return connect()
  }, [url])

  return { data, loading, error }
}

export default useWebSocket