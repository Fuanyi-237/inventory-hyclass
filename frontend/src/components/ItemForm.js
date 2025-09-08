import React, { useState, useEffect, useContext } from 'react';
import { TextField, Button, MenuItem, Box, Paper, Typography, Snackbar, Alert } from '@mui/material';
import apiClient from '../api';
import { AuthContext } from '../context/AuthContext';

function ItemForm({ onItemAdded }) {
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
      setSnackbar({ open: true, message: 'Item added successfully', severity: 'success' });
      if (onItemAdded) onItemAdded();
    } catch (err) {
      setSnackbar({ open: true, message: err?.message || String(err) || 'Failed to add item', severity: 'error' });
    }
  };

  return (
    <>
      <Paper sx={{ p: 3, mb: 2 }}>
        <Typography variant="h6" gutterBottom>Add New Item</Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <TextField id="add-item-unique-id" label="Unique ID" name="unique_id" value={form.unique_id} onChange={handleChange} fullWidth margin="normal" required />
          <TextField id="add-item-name" label="Name" name="name" value={form.name} onChange={handleChange} fullWidth margin="normal" required />
          <TextField id="add-item-description" label="Description" name="description" value={form.description} onChange={handleChange} fullWidth margin="normal" />
          <TextField id="add-item-category" select label="Category" name="category_id" value={form.category_id} onChange={handleChange} fullWidth margin="normal" required>
            {categories.map(cat => <MenuItem key={cat.id} value={cat.id}>{cat.name}</MenuItem>)}
          </TextField>
          <TextField id="add-item-state" select label="State" name="state" value={form.state} onChange={handleChange} fullWidth margin="normal">
            <MenuItem value="good">Good</MenuItem>
            <MenuItem value="moderate">Moderate</MenuItem>
            <MenuItem value="bad">Bad</MenuItem>
          </TextField>
          <TextField id="add-item-location" label="Location" name="location" value={form.location} onChange={handleChange} fullWidth margin="normal" />
          <TextField id="add-item-purchase-date" label="Purchase Date" name="purchase_date" type="date" value={form.purchase_date} onChange={handleChange} fullWidth margin="normal" InputLabelProps={{ shrink: true }} />
          <TextField id="add-item-expiry-date" label="Expiry Date" name="expiry_date" type="date" value={form.expiry_date} onChange={handleChange} fullWidth margin="normal" InputLabelProps={{ shrink: true }} />
          <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>Add Item</Button>
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
