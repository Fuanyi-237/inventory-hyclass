import React, { useState, useContext } from 'react';
import { TextField, Button, Box, Alert, Typography, InputAdornment, useTheme } from '@mui/material';
import Logo from '../components/Logo';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const theme = useTheme();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      // Validate inputs
      if (!username.trim() || !password) {
        throw new Error('Please enter both username and password');
      }
      
      // Attempt login
      await login(username, password);
      
      // Redirect to home on success
      navigate('/');
    } catch (err) {
      // Normalize FastAPI error shapes to a readable string
      const detail = err.response?.data?.detail;
      let errorMessage = '';
      if (Array.isArray(detail)) {
        errorMessage = detail
          .map((d) => d?.msg || (typeof d === 'string' ? d : JSON.stringify(d)))
          .join('; ');
      } else if (typeof detail === 'string') {
        errorMessage = detail;
      } else if (err.message) {
        errorMessage = err.message;
      } else {
        errorMessage = 'An error occurred during login. Please try again.';
      }
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: 'background.default',
        p: 2,
      }}
    >
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          width: '100%',
          maxWidth: 400,
          p: 3,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          bgcolor: 'background.paper',
          borderRadius: 2,
          boxShadow: 1,
        }}
      >
        <Box sx={{ mb: 3, textAlign: 'center' }}>
          <Logo size="medium" variant="vertical" />
          <Typography variant="h5" component="h1" sx={{ mt: 2, fontWeight: 600 }}>
            Welcome Back
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Sign in to your account
          </Typography>
        </Box>
        
        {error && (
          <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
            {error}
          </Alert>
        )}
      
        <TextField
          fullWidth
          label="Username"
          variant="outlined"
          margin="normal"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          autoComplete="username"
          autoFocus
          sx={{ mb: 2 }}
        />
        
        <TextField
          fullWidth
          label="Password"
          type={showPassword ? 'text' : 'password'}
          variant="outlined"
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="current-password"
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <Button
                  onClick={handleClickShowPassword}
                  size="small"
                  sx={{ 
                    textTransform: 'none',
                    color: 'primary.main',
                  }}
                >
                  {showPassword ? 'Hide' : 'Show'}
                </Button>
              </InputAdornment>
            ),
          }}
          sx={{ mb: 3 }}
        />
        
        <Button
          type="submit"
          fullWidth
          variant="contained"
          size="large"
          disabled={isLoading}
          sx={{
            py: 1.5,
            borderRadius: 1,
            textTransform: 'none',
            fontSize: '1rem',
            fontWeight: 500,
          }}
        >
          {isLoading ? 'Signing in...' : 'Sign In'}
        </Button>
        
        <Box sx={{ mt: 3, textAlign: 'center', width: '100%' }}>
          <Typography variant="body2" color="text.secondary">
            <a 
              href="mailto:admin@example.com"
              onClick={(e) => {
                e.preventDefault();
                window.location.href = 'mailto:admin@example.com';
              }}
              style={{
                color: theme.palette.primary.main,
                textDecoration: 'none',
                '&:hover': {
                  textDecoration: 'underline',
                },
              }}
            >
              Need access? Contact admin
            </a>
          </Typography>
        </Box>
      </Box>
    </Box>
  );
}

export default Login;
