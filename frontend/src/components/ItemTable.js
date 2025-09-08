import React, { useEffect, useState, useContext } from 'react';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, 
  Typography, TextField, MenuItem, Grid, Box, IconButton, Dialog, 
  DialogActions, DialogContent, DialogContentText, DialogTitle, Button 
} from '@mui/material';

import apiClient from '../api';
import { AuthContext } from '../context/AuthContext';

function ItemTable({ reload }) {
  const { user } = useContext(AuthContext);
  const [items, setItems] = useState([]);
  const [search, setSearch] = useState({ name: '', category: '', state: '' });
  const [categories, setCategories] = useState([]);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);

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

  const filtered = items.filter(item =>
    (!search.name || item.name.toLowerCase().includes(search.name.toLowerCase())) &&
    (!search.category || (item.category && item.category.name === search.category)) &&
    (!search.state || item.state === search.state)
  );

  return (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Typography variant="h6" sx={{ p: 2 }}>Inventory Items</Typography>
      <Box sx={{ p: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <TextField label="Search Name" value={search.name} onChange={e => setSearch(s => ({ ...s, name: e.target.value }))} fullWidth />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField select label="Category" value={search.category} onChange={e => setSearch(s => ({ ...s, category: e.target.value }))} fullWidth>
              <MenuItem value="">All</MenuItem>
              {categories.map(cat => <MenuItem key={cat.id} value={cat.name}>{cat.name}</MenuItem>)}
            </TextField>
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField select label="State" value={search.state} onChange={e => setSearch(s => ({ ...s, state: e.target.value }))} fullWidth>
              <MenuItem value="">All</MenuItem>
              <MenuItem value="good">Good</MenuItem>
              <MenuItem value="moderate">Moderate</MenuItem>
              <MenuItem value="bad">Bad</MenuItem>
            </TextField>
          </Grid>
        </Grid>
      </Box>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Unique ID</TableCell>
            <TableCell>Category</TableCell>
            <TableCell>State</TableCell>
            {user && user.role !== 'viewer' && <TableCell>Created By</TableCell>}
            {user && user.role !== 'viewer' && <TableCell>Last Modified By</TableCell>}
            <TableCell>Location</TableCell>
            <TableCell>Purchase Date</TableCell>
            <TableCell>Expiry Date</TableCell>
            <TableCell>Description</TableCell>
            {user && user.role !== 'viewer' && <TableCell>Actions</TableCell>}
          </TableRow>
        </TableHead>
        <TableBody>
          {filtered.map(item => (
            <TableRow key={item.id}>
              <TableCell>{item.id}</TableCell>
              <TableCell>{item.name}</TableCell>
              <TableCell>{item.unique_id}</TableCell>
              <TableCell>{item.category && typeof item.category === 'object' && item.category.name ? item.category.name : 'N/A'}</TableCell>
              <TableCell>{item.state}</TableCell>
              {user && user.role !== 'viewer' && <TableCell>{item.created_by_user ? item.created_by_user.username : 'N/A'}</TableCell>}
              {user && user.role !== 'viewer' && <TableCell>{item.last_modified_by_user ? item.last_modified_by_user.username : 'N/A'}</TableCell>}
              <TableCell>{item.location}</TableCell>
              <TableCell>{item.purchase_date ? new Date(item.purchase_date).toLocaleDateString() : ''}</TableCell>
              <TableCell>{item.expiry_date ? new Date(item.expiry_date).toLocaleDateString() : ''}</TableCell>
              <TableCell>{typeof item.description === 'string' ? item.description : (item.description && typeof item.description === 'object' ? JSON.stringify(item.description) : 'N/A')}</TableCell>
              {user && user.role !== 'viewer' && (
                <TableCell>
                  <Button onClick={() => handleDeleteClick(item)} color="error" size="small">
                    Delete
                  </Button>
                </TableCell>
              )}
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Dialog open={openDeleteDialog} onClose={handleCloseDeleteDialog}>
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete the item "{selectedItem?.name}"? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDeleteDialog}>Cancel</Button>
          <Button onClick={handleConfirmDelete} color="error">Delete</Button>
        </DialogActions>
      </Dialog>
    </TableContainer>
  );
}

export default ItemTable;
