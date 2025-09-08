import React, { useState } from 'react';
import { Container, Typography } from '@mui/material';
import UserForm from './UserForm';
import UserTable from './UserTable';
import UserMenu from './UserMenu';

function UserManagement() {
  const [reloadKey, setReloadKey] = useState(0);

  const handleUserAdded = () => {
    setReloadKey(prevKey => prevKey + 1); // Increment key to trigger reload
  };
  return (
    <>
      <UserMenu />
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          User Management
        </Typography>
        <UserForm onUserAdded={handleUserAdded} />
        <UserTable key={reloadKey} />
      </Container>
    </>
  );
}

export default UserManagement;

