import React, { useEffect, useState, useContext } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, TextField, MenuItem, Grid, Box, Button } from '@mui/material';
import apiClient from '../api';
import { AuthContext } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';

function TransactionTable() {
  const { user } = useContext(AuthContext);
  const { t } = useTranslation();
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
        <Typography variant="h6">{t('transactions.recent')}</Typography>
        {user && (
          <Button onClick={exportLastWeek} variant="outlined" size="small" disabled={downloading}>
            {downloading ? t('transactions.exporting') : t('transactions.exportLastWeek')}
          </Button>
        )}
      </Box>
      <Box sx={{ p: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <TextField label={t('transactions.filters.itemId')} value={search.item_id} onChange={e => setSearch(s => ({ ...s, item_id: e.target.value }))} fullWidth />
          </Grid>
          {user && user.role !== 'viewer' && (
            <Grid item xs={12} md={4}>
              <TextField label={t('transactions.filters.userId')} value={search.user_id} onChange={e => setSearch(s => ({ ...s, user_id: e.target.value }))} fullWidth />
            </Grid>
          )}
          <Grid item xs={12} md={4}>
            <TextField select label={t('transactions.filters.action')} value={search.action} onChange={e => setSearch(s => ({ ...s, action: e.target.value }))} fullWidth>
              <MenuItem value="">{t('common.all')}</MenuItem>
              <MenuItem value="sign_in">{t('transactions.sign_in')}</MenuItem>
              <MenuItem value="sign_out">{t('transactions.sign_out')}</MenuItem>
            </TextField>
          </Grid>
        </Grid>
      </Box>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>{t('common.id')}</TableCell>
            <TableCell>{t('transactions.itemId')}</TableCell>
            {user && user.role !== 'viewer' && <TableCell>{t('transactions.userId')}</TableCell>}
            <TableCell>{t('transactions.action')}</TableCell>
            <TableCell>{t('common.state')}</TableCell>
            <TableCell>{t('transactions.timestamp')}</TableCell>
            <TableCell>{t('transactions.notes')}</TableCell>
            <TableCell>{t('transactions.image')}</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {filtered.slice(-10).reverse().map(trx => (
            <TableRow key={trx.id}>
              <TableCell>{trx.id}</TableCell>
              <TableCell>{trx.item && typeof trx.item === 'object' && (typeof trx.item.id === 'string' || typeof trx.item.id === 'number') ? trx.item.id : t('common.n_a')}</TableCell>
              {user && user.role !== 'viewer' && <TableCell>{trx.user && typeof trx.user === 'object' && (typeof trx.user.id === 'string' || typeof trx.user.id === 'number') ? trx.user.id : t('common.n_a')}</TableCell>}
              <TableCell>{trx.action}</TableCell>
              <TableCell>{trx.state}</TableCell>
              <TableCell>{trx.timestamp ? new Date(trx.timestamp).toLocaleString() : ''}</TableCell>
              <TableCell>{typeof trx.notes === 'string' ? trx.notes : (trx.notes && typeof trx.notes === 'object' ? JSON.stringify(trx.notes) : t('common.n_a'))}</TableCell>
              <TableCell>
                {trx.image_url && (
                  <a href={`${trx.image_url}`} target="_blank" rel="noopener noreferrer">
                    {t('transactions.viewImage')}
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
