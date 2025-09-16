import React, { useEffect, useState, useContext } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button } from '@mui/material';

import apiClient from '../api';
import { AuthContext } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';

function CategoryTable({ reload }) {
  const [categories, setCategories] = useState([]);
  const { user } = useContext(AuthContext);
  const [editCat, setEditCat] = useState(null);
  const [editForm, setEditForm] = useState({ name: '', description: '' });
  const { t } = useTranslation();


  const fetchCategories = () => {
    apiClient.get('/categories/')
      .then(res => setCategories(res.data))
      .catch(() => setCategories([]));
  };

  useEffect(() => {
    if (user) {
      fetchCategories();
    }
    // eslint-disable-next-line
  }, [reload, user]);

  const handleEditOpen = (cat) => {
    setEditCat(cat);
    const description = cat.description && typeof cat.description === 'object' ? cat.description.name : cat.description;
    setEditForm({ name: cat.name, description: description || '' });
  };
  const handleEditClose = () => setEditCat(null);
  const handleEditChange = (e) => setEditForm({ ...editForm, [e.target.name]: e.target.value });
  const handleEditSave = async () => {
    await apiClient.put(`/categories/${editCat.id}/`, editForm);
    setEditCat(null);
    fetchCategories();
  };
  const handleDelete = async (id) => {
    if (window.confirm(t('categories.confirmDelete'))) {
      await apiClient.delete(`/categories/${id}/`);
      fetchCategories();
    }
  };

  return (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Typography variant="h6" sx={{ p: 2 }}>{t('categories.title')}</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>{t('common.id')}</TableCell>
            <TableCell>{t('common.name')}</TableCell>
            <TableCell>{t('common.description')}</TableCell>
            <TableCell>{t('common.actions')}</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {categories.map(cat => (
            <TableRow key={cat.id}>
              <TableCell>{cat.id}</TableCell>
              <TableCell>{cat.name}</TableCell>
              <TableCell>{
                !cat.description ? t('common.n_a') : 
                typeof cat.description === 'object' ? 
                  (cat.description.name || t('common.n_a')) : 
                  String(cat.description)
              }</TableCell>
              <TableCell>
                <Button color="primary" onClick={() => handleEditOpen(cat)}>{t('common.edit')}</Button>
                <Button color="error" onClick={() => handleDelete(cat.id)}>{t('common.delete')}</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Dialog open={!!editCat} onClose={handleEditClose}>
        <DialogTitle>{t('categories.editTitle')}</DialogTitle>
        <DialogContent>
          <TextField label={t('common.name')} name="name" value={editForm.name} onChange={handleEditChange} fullWidth margin="normal" />
          <TextField label={t('common.description')} name="description" value={editForm.description || ''} onChange={handleEditChange} fullWidth margin="normal" />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleEditClose}>{t('common.cancel')}</Button>
          <Button onClick={handleEditSave} variant="contained">{t('common.save')}</Button>
        </DialogActions>
      </Dialog>
    </TableContainer>
  );
}

export default CategoryTable;
