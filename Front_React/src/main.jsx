import './api/auth.js';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { UserProvider } from './components/UserContext.jsx';
import './index.css';
import App from './App.jsx';
import { HelmetProvider } from "react-helmet-async";



  createRoot(document.getElementById('root')).render(
    <StrictMode>
      <HelmetProvider>
        <BrowserRouter>
          <UserProvider>
            <App />
          </UserProvider>
        </BrowserRouter>
      </HelmetProvider>
    </StrictMode>
  );
