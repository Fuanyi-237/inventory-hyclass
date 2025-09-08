import React, { useState } from 'react';
import { TextField, Button, Box, Paper, Typography, Snackbar, Alert } from '@mui/material';
import apiClient from '../api';

function CategoryForm({ onCategoryAdded }) {
  const [form, setForm] = useState({ name: '', description: '' });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiClient.post('/categories/', form);
      setForm({ name: '', description: '' });
      setSnackbar({ open: true, message: 'Category added successfully', severity: 'success' });
      if (onCategoryAdded) onCategoryAdded();
    } catch (err) {
      setSnackbar({ open: true, message: err?.message || String(err) || 'Failed to add category', severity: 'error' });
    }
  };

  return (
    <>
      <Paper sx={{ p: 3, mb: 2 }}>
        <Typography variant="h6" gutterBottom>Add New Category</Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <TextField id="add-category-name" label="Name" name="name" value={form.name} onChange={handleChange} fullWidth margin="normal" required />
          <TextField id="add-category-description" label="Description" name="description" value={form.description} onChange={handleChange} fullWidth margin="normal" />
          <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>Add Category</Button>
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

export default CategoryForm;
