import React, { useEffect, useState, useContext } from 'react';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, 
  Typography, TextField, MenuItem, Grid, Box, IconButton, Dialog, 
  DialogActions, DialogContent, DialogContentText, DialogTitle, Button,
  Snackbar, Alert
} from '@mui/material';

import apiClient from '../api';
import { AuthContext } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';

function ItemTable({ reload }) {
  const { user } = useContext(AuthContext);
  const { t } = useTranslation();
  const [items, setItems] = useState([]);
  const [search, setSearch] = useState({ name: '', category: '', state: '' });
  const [categories, setCategories] = useState([]);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [editForm, setEditForm] = useState({
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
      apiClient.get('/items/')
        .then(res => setItems(res.data))
        .catch(() => setItems([]));
      apiClient.get('/categories/')
        .then(res => setCategories(res.data))
        .catch(() => setCategories([]));
    }
  }, [reload, user]);

  const handleDeleteClick = (item) => {
    setSelectedItem(item);
    setOpenDeleteDialog(true);
  };

  const handleCloseDeleteDialog = () => {
    setOpenDeleteDialog(false);
    setSelectedItem(null);
  };

  const handleConfirmDelete = () => {
    if (selectedItem) {
      apiClient.delete(`/items/${selectedItem.id}`)
        .then(() => {
          setItems(items.filter(i => i.id !== selectedItem.id));
          handleCloseDeleteDialog();
        })
        .catch(error => {
          console.error("Error deleting item:", error);
          handleCloseDeleteDialog();
        });
    }
  };

  const handleEditClick = (item) => {
    setSelectedItem(item);
    setEditForm({
      unique_id: item.unique_id || '',
      name: item.name || '',
      description: item.description || '',
      category_id: item.category?.id || '',
      state: item.state || 'good',
      location: item.location || '',
      purchase_date: item.purchase_date ? item.purchase_date.split('T')[0] : '',
      expiry_date: item.expiry_date ? item.expiry_date.split('T')[0] : ''
    });
    setOpenEditDialog(true);
  };

  const handleCloseEditDialog = () => {
    setOpenEditDialog(false);
    setSelectedItem(null);
    setEditForm({
      unique_id: '',
      name: '',
      description: '',
      category_id: '',
      state: 'good',
      location: '',
      purchase_date: '',
      expiry_date: ''
    });
  };

  const handleEditFormChange = (e) => {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  };

  const handleSaveEdit = async () => {
    try {
      const updateData = {
        ...editForm,
        category_id: Number(editForm.category_id),
        purchase_date: editForm.purchase_date ? new Date(editForm.purchase_date).toISOString() : null,
        expiry_date: editForm.expiry_date ? new Date(editForm.expiry_date).toISOString() : null
      };
      
      await apiClient.put(`/items/${selectedItem.id}`, updateData);
      
      // Update the item in the local state
      setItems(items.map(item => 
        item.id === selectedItem.id 
          ? { ...item, ...updateData, category: categories.find(cat => cat.id === updateData.category_id) }
          : item
      ));
      
      setSnackbar({ open: true, message: t('items.editSuccess'), severity: 'success' });
      handleCloseEditDialog();
    } catch (err) {
      setSnackbar({ open: true, message: err?.message || t('items.editFailed'), severity: 'error' });
    }
  };

  const filtered = items.filter(item =>
    (!search.name || item.name.toLowerCase().includes(search.name.toLowerCase())) &&
    (!search.category || (item.category && item.category.name === search.category)) &&
    (!search.state || item.state === search.state)
  );

  return (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Typography variant="h6" sx={{ p: 2 }}>{t('items.title')}</Typography>
      <Box sx={{ p: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <TextField label={t('items.searchName')} value={search.name} onChange={e => setSearch(s => ({ ...s, name: e.target.value }))} fullWidth />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField select label={t('common.category')} value={search.category} onChange={e => setSearch(s => ({ ...s, category: e.target.value }))} fullWidth>
              <MenuItem value="">{t('common.all')}</MenuItem>
              {categories.map(cat => <MenuItem key={cat.id} value={cat.name}>{cat.name}</MenuItem>)}
            </TextField>
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField select label={t('common.state')} value={search.state} onChange={e => setSearch(s => ({ ...s, state: e.target.value }))} fullWidth>
              <MenuItem value="">{t('common.all')}</MenuItem>
              <MenuItem value="good">{t('items.state.good')}</MenuItem>
              <MenuItem value="moderate">{t('items.state.moderate')}</MenuItem>
              <MenuItem value="bad">{t('items.state.bad')}</MenuItem>
            </TextField>
          </Grid>
        </Grid>
      </Box>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>{t('common.id')}</TableCell>
            <TableCell>{t('common.name')}</TableCell>
            <TableCell>{t('items.uniqueId')}</TableCell>
            <TableCell>{t('common.category')}</TableCell>
            <TableCell>{t('common.state')}</TableCell>
            {user && user.role !== 'viewer' && <TableCell>{t('items.createdBy')}</TableCell>}
            {user && user.role !== 'viewer' && <TableCell>{t('items.lastModifiedBy')}</TableCell>}
            <TableCell>{t('items.location')}</TableCell>
            <TableCell>{t('items.purchaseDate')}</TableCell>
            <TableCell>{t('items.expiryDate')}</TableCell>
            <TableCell>{t('common.description')}</TableCell>
            {user && user.role !== 'viewer' && <TableCell>{t('common.actions')}</TableCell>}
          </TableRow>
        </TableHead>
        <TableBody>
          {filtered.map(item => (
            <TableRow key={item.id}>
              <TableCell>{item.id}</TableCell>
              <TableCell>{item.name}</TableCell>
              <TableCell>{item.unique_id}</TableCell>
              <TableCell>{item.category && typeof item.category === 'object' && item.category.name ? item.category.name : t('common.n_a')}</TableCell>
              <TableCell>{item.state}</TableCell>
              {user && user.role !== 'viewer' && <TableCell>{item.created_by_user ? item.created_by_user.username : t('common.n_a')}</TableCell>}
              {user && user.role !== 'viewer' && <TableCell>{item.last_modified_by_user ? item.last_modified_by_user.username : t('common.n_a')}</TableCell>}
              <TableCell>{item.location}</TableCell>
              <TableCell>{item.purchase_date ? new Date(item.purchase_date).toLocaleDateString() : ''}</TableCell>
              <TableCell>{item.expiry_date ? new Date(item.expiry_date).toLocaleDateString() : ''}</TableCell>
              <TableCell>{typeof item.description === 'string' ? item.description : (item.description && typeof item.description === 'object' ? JSON.stringify(item.description) : t('common.n_a'))}</TableCell>
              {user && user.role !== 'viewer' && (
                <TableCell>
                  <Button onClick={() => handleEditClick(item)} color="primary" size="small" sx={{ mr: 1 }}>
                    {t('common.edit')}
                  </Button>
                  <Button onClick={() => handleDeleteClick(item)} color="error" size="small">
                    {t('common.delete')}
                  </Button>
                </TableCell>
              )}
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Dialog open={openDeleteDialog} onClose={handleCloseDeleteDialog}>
        <DialogTitle>{t('items.confirmDeletion')}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {t('items.confirmDeleteMessage', { name: selectedItem?.name || '' })}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDeleteDialog}>{t('common.cancel')}</Button>
          <Button onClick={handleConfirmDelete} color="error">{t('common.delete')}</Button>
        </DialogActions>
      </Dialog>

      <Dialog open={openEditDialog} onClose={handleCloseEditDialog} maxWidth="md" fullWidth>
        <DialogTitle>{t('items.editTitle')}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <TextField
                label={t('items.uniqueId')}
                name="unique_id"
                value={editForm.unique_id}
                onChange={handleEditFormChange}
                fullWidth
                required
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label={t('common.name')}
                name="name"
                value={editForm.name}
                onChange={handleEditFormChange}
                fullWidth
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label={t('common.description')}
                name="description"
                value={editForm.description}
                onChange={handleEditFormChange}
                fullWidth
                multiline
                rows={2}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                select
                label={t('common.category')}
                name="category_id"
                value={editForm.category_id}
                onChange={handleEditFormChange}
                fullWidth
                required
              >
                {categories.map(cat => (
                  <MenuItem key={cat.id} value={cat.id}>{cat.name}</MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                select
                label={t('common.state')}
                name="state"
                value={editForm.state}
                onChange={handleEditFormChange}
                fullWidth
              >
                <MenuItem value="good">{t('items.state.good')}</MenuItem>
                <MenuItem value="moderate">{t('items.state.moderate')}</MenuItem>
                <MenuItem value="bad">{t('items.state.bad')}</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label={t('items.location')}
                name="location"
                value={editForm.location}
                onChange={handleEditFormChange}
                fullWidth
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label={t('items.purchaseDate')}
                name="purchase_date"
                type="date"
                value={editForm.purchase_date}
                onChange={handleEditFormChange}
                fullWidth
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label={t('items.expiryDate')}
                name="expiry_date"
                type="date"
                value={editForm.expiry_date}
                onChange={handleEditFormChange}
                fullWidth
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseEditDialog}>{t('common.cancel')}</Button>
          <Button onClick={handleSaveEdit} variant="contained" color="primary">
            {t('common.save')}
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar open={snackbar.open} autoHideDuration={4000} onClose={() => setSnackbar({ ...snackbar, open: false })}>
        <Alert onClose={() => setSnackbar({ ...snackbar, open: false })} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </TableContainer>
  );
}

export default ItemTable;
