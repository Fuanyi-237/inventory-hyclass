import React, { useState, useEffect, useContext } from 'react';
import { Box, Paper, Typography, Button, MenuItem, TextField, Grid, Snackbar, Alert } from '@mui/material';
import apiClient from '../api';
import { AuthContext } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';

function SignInOutForm({ onTransaction }) {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({
    item_id: '',
    action: 'sign_out',
    notes: '',
    state: 'good'
  });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const [imageFile, setImageFile] = useState(null);
  const { user } = useContext(AuthContext);
  const { t } = useTranslation();

  useEffect(() => {
    apiClient.get('/items/')
      .then(res => setItems(res.data))
      .catch(() => setItems([]));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      setSnackbar({ open: true, message: t('auth.notAuthenticated'), severity: 'error' });
      return;
    }

    let imageUrl = null;
    if (imageFile) {
      const formData = new FormData();
      formData.append('file', imageFile);

      try {
        const response = await apiClient.post('/uploads/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        imageUrl = response.data.image_url;
      } catch (error) {
        setSnackbar({ open: true, message: t('uploads.failed'), severity: 'error' });
        return;
      }
    }

    try {
      await apiClient.post('/transactions/', {
        ...form,
        item_id: Number(form.item_id),
        user_id: user.id,
        timestamp: new Date().toISOString(),
        state: form.state,
        image_url: imageUrl,
      });
      setForm({ item_id: '', action: 'sign_out', notes: '', state: 'good' });
      setImageFile(null);
      // Also reset the file input if it exists (it's only rendered for moderate/bad state)
      const fileInput = document.getElementById('signinout-image-upload');
      if (fileInput) {
        fileInput.value = null;
      }
      setSnackbar({ open: true, message: t('transactions.success'), severity: 'success' });
      if (onTransaction) onTransaction();
    } catch (err) {
      setSnackbar({ open: true, message: t('transactions.failed'), severity: 'error' });
    }
  };

  return (
    <>
      <Paper sx={{ p: 3, mb: 2 }}>
        <Typography variant="h6" gutterBottom>{t('transactions.signInOutTitle')}</Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <TextField id="signinout-item" select label={t('items.item') || 'Item'} name="item_id" value={form.item_id} onChange={handleChange} fullWidth required>
                {items.map(item => <MenuItem key={item.id} value={item.id}>{item.name} ({item.unique_id})</MenuItem>)}
              </TextField>
            </Grid>
            <Grid item xs={12} md={2}>
              <TextField id="signinout-action" select label={t('transactions.action')} name="action" value={form.action} onChange={handleChange} fullWidth>
                <MenuItem value="sign_out">{t('transactions.sign_out')}</MenuItem>
                <MenuItem value="sign_in">{t('transactions.sign_in')}</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} md={2}>
              <TextField id="signinout-state" select label={t('common.state')} name="state" value={form.state} onChange={handleChange} fullWidth>
                <MenuItem value="good">{t('items.state.good')}</MenuItem>
                <MenuItem value="moderate">{t('items.state.moderate')}</MenuItem>
                <MenuItem value="bad">{t('items.state.bad')}</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField id="signinout-notes" label={t('transactions.notes')} name="notes" value={form.notes} onChange={handleChange} fullWidth />
            </Grid>
            {(form.state === 'moderate' || form.state === 'bad') && (
              <Grid item xs={12}>
                <TextField
                  id="signinout-image-upload"
                  type="file"
                  onChange={(e) => setImageFile(e.target.files[0])}
                  fullWidth
                  InputLabelProps={{
                    shrink: true,
                  }}
                  label={t('uploads.label')}
                  helperText={t('uploads.helper')}
                />
              </Grid>
            )}
          </Grid>
          <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>{t('common.save')}</Button>
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

export default SignInOutForm;
