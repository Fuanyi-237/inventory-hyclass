import React, { useContext } from 'react';
import { AppBar, Toolbar, Button, Box, Avatar, Typography, Divider, IconButton, MenuItem, Select } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import Logo from './Logo';
import { useTranslation } from 'react-i18next';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();

  const currentLang = i18n.language || 'en';
  const handleLangChange = (e) => {
    const lang = e.target.value;
    i18n.changeLanguage(lang);
    try { localStorage.setItem('lang', lang); } catch {}
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <AppBar 
      position="fixed" 
      elevation={1}
      sx={{
        background: 'white',
        borderBottom: '1px solid rgba(0, 0, 0, 0.08)',
        color: 'primary.main',
        zIndex: (theme) => theme.zIndex.drawer + 1
      }}
    >
      <Toolbar 
        disableGutters
        sx={{ 
          minHeight: '64px',
          px: { xs: 2, md: 3 },
          mx: 'auto',
          width: '100%',
          maxWidth: '1600px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <Box sx={{ 
          display: 'flex', 
          alignItems: 'center',
          height: '100%',
          '& .MuiBox-root': {  // Target the LogoContainer
            height: '100%',
            padding: '8px 0',
          }
        }}>
          <Logo size="medium" />
          <Divider 
            orientation="vertical" 
            flexItem 
            sx={{ 
              height: '32px', 
              mx: 1.5,
              my: 'auto',
              borderColor: 'rgba(0, 0, 0, 0.12)'
            }} 
          />
          <Button 
            component={RouterLink} 
            to="/"
            sx={{ 
              textTransform: 'none', 
              fontWeight: 500,
              color: 'text.primary',
              '&:hover': {
                color: 'primary.main',
                backgroundColor: 'rgba(26, 35, 126, 0.04)'
              }
            }}
          >
            {t('common.dashboard')}
          </Button>
          {(user?.role === 'admin' || user?.role === 'superadmin' || (typeof user?.role === 'string' && user.role.toLowerCase().includes('admin'))) && (
            <Button 
              component={RouterLink} 
              to="/users"
              sx={{ 
                textTransform: 'none', 
                fontWeight: 500,
                color: 'text.primary',
                '&:hover': {
                  color: 'primary.main',
                  backgroundColor: 'rgba(26, 35, 126, 0.04)'
                }
              }}
            >
              {t('common.userManagement')}
            </Button>
          )}
        </Box>
        
        {user ? (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Select
              value={currentLang}
              size="small"
              onChange={handleLangChange}
              variant="outlined"
              sx={{ mr: 1, height: 32 }}
            >
              <MenuItem value="en">EN</MenuItem>
              <MenuItem value="fr">FR</MenuItem>
            </Select>
            <Box sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: 1,
              px: 2,
              py: 1,
              borderRadius: 1,
              '&:hover': {
                backgroundColor: 'rgba(0, 0, 0, 0.04)'
              }
            }}>
              <Avatar 
                sx={{ 
                  bgcolor: 'primary.main', 
                  width: 32, 
                  height: 32,
                  color: 'white',
                  fontWeight: 600
                }}
              >
                {user.username.charAt(0).toUpperCase()}
              </Avatar>
              <Typography variant="body2" fontWeight={500}>
                {user.username}
              </Typography>
            </Box>
            <Button 
              onClick={handleLogout}
              variant="outlined"
              size="small"
              sx={{ 
                textTransform: 'none',
                fontWeight: 500,
                borderColor: 'divider',
                color: 'text.primary',
                '&:hover': {
                  borderColor: 'primary.main',
                  backgroundColor: 'rgba(26, 35, 126, 0.04)'
                }
              }}
            >
              {t('common.logout')}
            </Button>
          </Box>
        ) : (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Select
              value={currentLang}
              size="small"
              onChange={handleLangChange}
              variant="outlined"
              sx={{ height: 32 }}
            >
              <MenuItem value="en">EN</MenuItem>
              <MenuItem value="fr">FR</MenuItem>
            </Select>
            <Button 
            variant="contained" 
            component={RouterLink} 
            to="/login"
            size="small"
            sx={{
              textTransform: 'none',
              fontWeight: 500,
              backgroundColor: 'primary.main',
              '&:hover': {
                backgroundColor: 'primary.dark'
              }
            }}
          >
            {t('common.login')}
          </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
