import express from 'express'
import { exec } from 'child_process'
import path from 'path'
import fs from 'fs'
import { promisify } from 'util'

const execAsync = promisify(exec)
const app = express()
const PORT = 3002

app.use(express.json())
app.use(express.static('public'))

// Serve static files from AUTOMACAO directory
app.use('/AUTOMACAO', express.static(path.join(process.cwd(), '..', 'AUTOMACAO')))

// Execute Python script
app.post('/api/execute-script', async (req, res) => {
  try {
    const { script_path, working_directory } = req.body
    
    const fullScriptPath = path.join(working_directory, script_path)
    
    // Check if script exists
    if (!fs.existsSync(fullScriptPath)) {
      return res.status(404).json({ error: 'Script not found', path: fullScriptPath })
    }
    
    // Execute Python script
    const { stdout, stderr } = await execAsync(`python "${fullScriptPath}"`, {
      cwd: working_directory,
      timeout: 300000 // 5 minutes timeout
    })
    
    res.json({
      success: true,
      stdout: stdout,
      stderr: stderr,
      script: script_path
    })
    
  } catch (error) {
    console.error('Script execution error:', error)
    res.status(500).json({
      success: false,
      error: error.message,
      script: req.body.script_path
    })
  }
})

// Test Supabase connections
app.post('/api/test-supabase', async (req, res) => {
  try {
    // This would test actual Supabase connections
    // For now, return mock data based on .env file existence
    const envPath = path.join(process.cwd(), '..', '.env')
    const envExists = fs.existsSync(envPath)
    
    res.json({
      vcm_central: envExists,
      lifeway_rag: envExists,
      timestamp: new Date().toISOString()
    })
    
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
})

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() })
})

app.listen(PORT, () => {
  console.log(`🚀 VCM Backend Server running on http://localhost:${PORT}`)
  console.log(`📁 Serving static files from: ${path.join(process.cwd(), '..', 'AUTOMACAO')}`)
})