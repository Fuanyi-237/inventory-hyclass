import React, { useEffect, useState, useContext } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, TextField, MenuItem, Grid, Box, Button } from '@mui/material';
import apiClient from '../api';
import { AuthContext } from '../context/AuthContext';

function TransactionTable() {
  const { user } = useContext(AuthContext);
  const [transactions, setTransactions] = useState([]);
  const [search, setSearch] = useState({ item_id: '', user_id: '', action: '' });
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    if (user) {
      apiClient.get('/transactions/')
        .then(res => setTransactions(res.data))
        .catch(() => setTransactions([]));
    }
  }, [user]);

  const filtered = transactions.filter(trx => {
    const itemMatch = !search.item_id || (trx.item && String(trx.item.id) === search.item_id);
    const userMatch = !search.user_id || (trx.user && String(trx.user.id) === search.user_id);
    const actionMatch = !search.action || trx.action === search.action;
    return itemMatch && userMatch && actionMatch;
  });

  const exportLastWeek = async () => {
    try {
      setDownloading(true);
      const end = new Date();
      const start = new Date();
      start.setDate(end.getDate() - 7);
      const startISO = start.toISOString();
      const endISO = end.toISOString();
      const response = await apiClient.get(`/transactions/export`, {
        params: { start: startISO, end: endISO },
        responseType: 'blob',
      });
      const blob = new Blob([response.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `transactions_${startISO.slice(0,10)}_${endISO.slice(0,10)}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Export failed', e);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="h6">Recent Transactions</Typography>
        {user && (
          <Button onClick={exportLastWeek} variant="outlined" size="small" disabled={downloading}>
            {downloading ? 'Exporting…' : 'Export Last Week'}
          </Button>
        )}
      </Box>
      <Box sx={{ p: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <TextField label="Item ID" value={search.item_id} onChange={e => setSearch(s => ({ ...s, item_id: e.target.value }))} fullWidth />
          </Grid>
          {user && user.role !== 'viewer' && (
            <Grid item xs={12} md={4}>
              <TextField label="User ID" value={search.user_id} onChange={e => setSearch(s => ({ ...s, user_id: e.target.value }))} fullWidth />
            </Grid>
          )}
          <Grid item xs={12} md={4}>
            <TextField select label="Action" value={search.action} onChange={e => setSearch(s => ({ ...s, action: e.target.value }))} fullWidth>
              <MenuItem value="">All</MenuItem>
              <MenuItem value="sign_in">Sign In</MenuItem>
              <MenuItem value="sign_out">Sign Out</MenuItem>
            </TextField>
          </Grid>
        </Grid>
      </Box>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Item ID</TableCell>
            {user && user.role !== 'viewer' && <TableCell>User ID</TableCell>}
            <TableCell>Action</TableCell>
            <TableCell>State</TableCell>
            <TableCell>Timestamp</TableCell>
            <TableCell>Notes</TableCell>
            <TableCell>Image</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {filtered.slice(-10).reverse().map(trx => (
            <TableRow key={trx.id}>
              <TableCell>{trx.id}</TableCell>
              <TableCell>{trx.item && typeof trx.item === 'object' && (typeof trx.item.id === 'string' || typeof trx.item.id === 'number') ? trx.item.id : 'N/A'}</TableCell>
              {user && user.role !== 'viewer' && <TableCell>{trx.user && typeof trx.user === 'object' && (typeof trx.user.id === 'string' || typeof trx.user.id === 'number') ? trx.user.id : 'N/A'}</TableCell>}
              <TableCell>{trx.action}</TableCell>
              <TableCell>{trx.state}</TableCell>
              <TableCell>{trx.timestamp ? new Date(trx.timestamp).toLocaleString() : ''}</TableCell>
              <TableCell>{typeof trx.notes === 'string' ? trx.notes : (trx.notes && typeof trx.notes === 'object' ? JSON.stringify(trx.notes) : 'N/A')}</TableCell>
              <TableCell>
                {trx.image_url && (
                  <a href={`http://localhost:8000${trx.image_url}`} target="_blank" rel="noopener noreferrer">
                    View Image
                  </a>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default TransactionTable;
