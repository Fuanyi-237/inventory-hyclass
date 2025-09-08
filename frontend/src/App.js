import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { CssBaseline, ThemeProvider, Box } from '@mui/material';
import Logo from './components/Logo';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import UserManagement from './components/UserManagement';
import { AuthProvider, AuthContext } from './context/AuthContext';
import { useContext } from 'react';
import theme from './theme';
import Navbar from './components/Navbar';

function PrivateRoute({ children }) {
  const { user } = useContext(AuthContext);
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return (
    <>
      <Navbar />
      <Box sx={{ p: 3 }}>
        {children}
      </Box>
    </>
  );
}

function PublicRoute({ children }) {
  return (
    <Box sx={{ 
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%)',
      p: 3
    }}>
      <Box sx={{ 
        maxWidth: 400, 
        width: '100%',
        bgcolor: 'background.paper',
        p: 4,
        borderRadius: 2,
        boxShadow: 3
      }}>
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <Logo size="large" />
        </Box>
        {children}
      </Box>
    </Box>
  );
}

function App() {
  return (
    <AuthProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Routes>
            <Route path="/" element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            } />
            <Route path="/users" element={
              <PrivateRoute>
                <UserManagement />
              </PrivateRoute>
            } />
            <Route path="/login" element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            } />
          </Routes>
        </Router>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;
