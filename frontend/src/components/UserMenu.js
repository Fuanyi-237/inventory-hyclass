import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, IconButton, Menu, MenuItem, Avatar, Box } from '@mui/material';
import { AuthContext } from '../context/AuthContext';


function UserMenu() {
  const { user, logout } = useContext(AuthContext);
  const [anchorEl, setAnchorEl] = React.useState(null);
  const navigate = useNavigate();

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleLogout = () => {
    logout();
    handleClose();
  };

  if (!user) {
    return null;
  }

  return (
    <AppBar position="static" color="default" elevation={1}>
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Inventory Management
        </Typography>
        <Typography variant="h6" sx={{ mr: 2 }}>
          Welcome, {user.username} ({user.role})
        </Typography>
        <IconButton onClick={handleMenu} color="inherit">
          <Avatar>{user.username[0].toUpperCase()}</Avatar>
        </IconButton>
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleClose}
        >
          {user.role === 'superadmin' && (
            <MenuItem onClick={() => { navigate('/users'); handleClose(); }}>
              User Management
            </MenuItem>
          )}
          <MenuItem onClick={handleLogout}>Logout</MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
}

export default UserMenu;
