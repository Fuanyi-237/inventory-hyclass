import React, { useState, useEffect, useContext } from 'react';
import { TextField, Button, MenuItem, Box, Paper, Typography, Snackbar, Alert } from '@mui/material';
import apiClient from '../api';
import { AuthContext } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';

function ItemForm({ onItemAdded }) {
  const { t } = useTranslation();
  const { user } = useContext(AuthContext);
  const [categories, setCategories] = useState([]);
  const [form, setForm] = useState({
    unique_id: '',
    name: '',
    description: '',
    category_id: '',
    state: 'good',
    location: '',
    purchase_date: '',
    expiry_date: ''
  });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  useEffect(() => {
    if (user) {
      apiClient.get('/categories/')
        .then(res => setCategories(res.data))
        .catch(() => setCategories([]));
    }
  }, [user]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiClient.post('/items/', {
        ...form,
        category_id: Number(form.category_id),
        purchase_date: form.purchase_date ? new Date(form.purchase_date).toISOString() : null,
        expiry_date: form.expiry_date ? new Date(form.expiry_date).toISOString() : null
      });
      setForm({ unique_id: '', name: '', description: '', category_id: '', state: 'good', location: '', purchase_date: '', expiry_date: '' });
      setSnackbar({ open: true, message: t('items.addedSuccess'), severity: 'success' });
      if (onItemAdded) onItemAdded();
    } catch (err) {
      setSnackbar({ open: true, message: err?.message || String(err) || t('items.addFailed'), severity: 'error' });
    }
  };

  return (
    <>
      <Paper sx={{ p: 3, mb: 2 }}>
        <Typography variant="h6" gutterBottom>{t('items.title')}</Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <TextField id="add-item-unique-id" label={t('items.uniqueId')} name="unique_id" value={form.unique_id} onChange={handleChange} fullWidth margin="normal" required />
          <TextField id="add-item-name" label={t('common.name')} name="name" value={form.name} onChange={handleChange} fullWidth margin="normal" required />
          <TextField id="add-item-description" label={t('common.description')} name="description" value={form.description} onChange={handleChange} fullWidth margin="normal" />
          <TextField id="add-item-category" select label={t('common.category')} name="category_id" value={form.category_id} onChange={handleChange} fullWidth margin="normal" required>
            {categories.map(cat => <MenuItem key={cat.id} value={cat.id}>{cat.name}</MenuItem>)}
          </TextField>
          <TextField id="add-item-state" select label={t('common.state')} name="state" value={form.state} onChange={handleChange} fullWidth margin="normal">
            <MenuItem value="good">{t('items.state.good')}</MenuItem>
            <MenuItem value="moderate">{t('items.state.moderate')}</MenuItem>
            <MenuItem value="bad">{t('items.state.bad')}</MenuItem>
          </TextField>
          <TextField id="add-item-location" label={t('items.location')} name="location" value={form.location} onChange={handleChange} fullWidth margin="normal" />
          <TextField id="add-item-purchase-date" label={t('items.purchaseDate')} name="purchase_date" type="date" value={form.purchase_date} onChange={handleChange} fullWidth margin="normal" InputLabelProps={{ shrink: true }} />
          <TextField id="add-item-expiry-date" label={t('items.expiryDate')} name="expiry_date" type="date" value={form.expiry_date} onChange={handleChange} fullWidth margin="normal" InputLabelProps={{ shrink: true }} />
          <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>{t('items.create')}</Button>
        </Box>
      </Paper>
      <Snackbar open={snackbar.open} autoHideDuration={4000} onClose={() => setSnackbar({ ...snackbar, open: false })}>
        <Alert onClose={() => setSnackbar({ ...snackbar, open: false })} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </>
  );
}

export default ItemForm;
