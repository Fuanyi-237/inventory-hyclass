import React, { useState, useEffect } from 'react';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, 
  Button, Select, MenuItem, FormControl, InputLabel, Typography, Box 
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import apiClient from '../api';
import { AuthContext } from '../context/AuthContext';
import { useContext } from 'react';

function UserTable() {
  const { t } = useTranslation();
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
    return <Typography>{t('users.noPermission')}</Typography>;
  }

  return (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Typography variant="h6" sx={{ p: 2 }}>{t('users.management')}</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>{t('users.id')}</TableCell>
            <TableCell>{t('users.username')}</TableCell>
            <TableCell>{t('users.fullName')}</TableCell>
            <TableCell>{t('users.email')}</TableCell>
            <TableCell>{t('users.role')}</TableCell>
            <TableCell>{t('users.active')}</TableCell>
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
                    <MenuItem value="superadmin">{t('users.roles.superadmin')}</MenuItem>
                    <MenuItem value="admin">{t('users.roles.admin')}</MenuItem>
                    <MenuItem value="viewer">{t('users.roles.viewer')}</MenuItem>
                  </Select>
                </FormControl>
              </TableCell>
              <TableCell>{row.is_active ? t('common.yes') : t('common.no')}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default UserTable;
