import React, { useState, useContext } from 'react';
import { Container, Typography, Grid, Box, Tabs, Tab, AppBar } from '@mui/material';
import { useTranslation } from 'react-i18next';
import InventoryIcon from '@mui/icons-material/Inventory';
import CategoryIcon from '@mui/icons-material/Category';
import ReceiptLongIcon from '@mui/icons-material/ReceiptLong';
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import ItemForm from '../components/ItemForm';
import ItemTable from '../components/ItemTable';
import CategoryForm from '../components/CategoryForm';
import CategoryTable from '../components/CategoryTable';
import SignInOutForm from '../components/SignInOutForm';
import TransactionTable from '../components/TransactionTable';
import ItemStats from '../components/ItemStats';
import UserMenu from '../components/UserMenu';
import UserTable from '../components/UserTable';
import { AuthContext } from '../context/AuthContext';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

function Dashboard() {
  const { t } = useTranslation();
  const { user } = useContext(AuthContext);
  const [reload, setReload] = useState(false);
  const [catReload, setCatReload] = useState(false);
  const [transReload, setTransReload] = useState(false);
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleItemAdded = () => {
    setReload(r => !r);
  };

  const handleCategoryAdded = () => {
    setCatReload(r => !r);
  };

  const handleTransactionMade = () => {
    setTransReload(r => !r);
  };

  return (
    <>
      <UserMenu />
      <Container maxWidth="xl" sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>{t('dashboard.title')}</Typography>
        <Box sx={{ width: '100%' }}>
          <AppBar position="static" sx={{ backgroundColor: '#f5f5f5', color: 'black', boxShadow: '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)' }}>
            <Tabs 
              value={tabValue} 
              onChange={handleTabChange} 
              aria-label="dashboard tabs" 
              variant="fullWidth"
              indicatorColor="primary"
              textColor="primary"
            >
              <Tab label={t('dashboard.tabs.items')} {...a11yProps(0)} />
              <Tab label={t('dashboard.tabs.categories')} {...a11yProps(1)} />
              <Tab label={t('dashboard.tabs.transactions')} {...a11yProps(2)} />
              {user && user.role === 'superadmin' && <Tab label={t('dashboard.tabs.userManagement')} {...a11yProps(3)} />}
            </Tabs>
          </AppBar>
          <TabPanel value={tabValue} index={0}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <ItemStats />
              </Grid>
              <Grid item xs={12}>
                <ItemTable reload={reload} />
              </Grid>
              {user && user.role !== 'viewer' && (
                <Grid item xs={12}>
                  <ItemForm onItemAdded={handleItemAdded} />
                </Grid>
              )}
            </Grid>
          </TabPanel>
          <TabPanel value={tabValue} index={1}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={user && user.role !== 'viewer' ? 8 : 12}>
                <CategoryTable reload={catReload} />
              </Grid>
              {user && user.role !== 'viewer' && (
                <Grid item xs={12} md={4}>
                  <CategoryForm onCategoryAdded={handleCategoryAdded} />
                </Grid>
              )}
            </Grid>
          </TabPanel>
          <TabPanel value={tabValue} index={2}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TransactionTable reload={transReload} />
              </Grid>
              {user && user.role !== 'viewer' && (
                <Grid item xs={12}>
                  <SignInOutForm onTransaction={handleTransactionMade} />
                </Grid>
              )}
            </Grid>
          </TabPanel>
          {user && user.role === 'superadmin' && (
            <TabPanel value={tabValue} index={3}>
              <UserTable />
            </TabPanel>
          )}
        </Box>
      </Container>
    </>
  );
}

export default Dashboard;
