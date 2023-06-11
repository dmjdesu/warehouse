import '@popperjs/core';
import React from 'react';
import { createRoot } from 'react-dom/client';
// import '../css/index.css'

import App from './App.jsx';

createRoot(document.getElementById('app')).render(<App />);