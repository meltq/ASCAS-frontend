import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import Navbar from './Navbar.jsx'
import App_new from './App_new.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Navbar /> 
    <App_new />
  </StrictMode>,
)
