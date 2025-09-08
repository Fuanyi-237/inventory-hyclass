import React, { useEffect, useState, useContext } from 'react';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, 
  Typography, Select, MenuItem, FormControl, Box 
} from '@mui/material';
import apiClient from '../api';
import { AuthContext } from '../context/AuthContext';

function UserTable() {
  const [users, setUsers] = useState([]);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    if (user?.role === 'superadmin') {
      apiClient.get('/users/')
        .then(res => setUsers(res.data))
        .catch(err => console.error("Failed to fetch users:", err));
    }
  }, [user]);

  const handleRoleChange = (userId, newRole) => {
    apiClient.put(`/users/${userId}/role`, { role: newRole })
      .then(res => {
        setUsers(users.map(u => (u.id === userId ? res.data : u)));
      })
      .catch(err => console.error(`Failed to update role for user ${userId}:`, err));
  };

  if (user?.role !== 'superadmin') {
    return <Typography>You do not have permission to view this page.</Typography>;
  }

  return (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Typography variant="h6" sx={{ p: 2 }}>User Management</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Username</TableCell>
            <TableCell>Full Name</TableCell>
            <TableCell>Email</TableCell>
            <TableCell>Role</TableCell>
            <TableCell>Active</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {users.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.id}</TableCell>
              <TableCell>{row.username}</TableCell>
              <TableCell>{row.full_name}</TableCell>
              <TableCell>{row.email}</TableCell>
              <TableCell>
                <FormControl size="small">
                  <Select
                    value={row.role}
                    onChange={(e) => handleRoleChange(row.id, e.target.value)}
                  >
                    <MenuItem value="superadmin">Superadmin</MenuItem>
                    <MenuItem value="admin">Admin</MenuItem>
                    <MenuItem value="viewer">Viewer</MenuItem>
                  </Select>
                </FormControl>
              </TableCell>
              <TableCell>{row.is_active ? 'Yes' : 'No'}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default UserTable;
