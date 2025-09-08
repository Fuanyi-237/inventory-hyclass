import React, { useEffect, useState, useContext } from 'react';
import { Grid, Paper, Typography } from '@mui/material';
import apiClient from '../api';
import { AuthContext } from '../context/AuthContext';

function ItemStats() {
  const { user } = useContext(AuthContext);
  const [stats, setStats] = useState({ good: 0, moderate: 0, bad: 0 });

  useEffect(() => {
    if (user) {
      apiClient.get('/items/')
        .then(res => {
          const counts = { good: 0, moderate: 0, bad: 0 };
          res.data.forEach(item => {
            if (item.state === 'good') counts.good++;
            if (item.state === 'moderate') counts.moderate++;
            if (item.state === 'bad') counts.bad++;
          });
          setStats(counts);
        });
      }
  }, [user]);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={4}>
        <Paper sx={{ p: 2, bgcolor: '#e3f2fd', textAlign: 'center' }}>
          <Typography variant="h6">Good</Typography>
          <Typography variant="h4" fontWeight="bold" color="#388e3c">{stats.good}</Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} md={4}>
        <Paper sx={{ p: 2, bgcolor: '#fffde7', textAlign: 'center' }}>
          <Typography variant="h6">Moderate</Typography>
          <Typography variant="h4" fontWeight="bold" color="#fbc02d">{stats.moderate}</Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} md={4}>
        <Paper sx={{ p: 2, bgcolor: '#ffebee', textAlign: 'center' }}>
          <Typography variant="h6">Bad</Typography>
          <Typography variant="h4" fontWeight="bold" color="#d32f2f">{stats.bad}</Typography>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default ItemStats;
