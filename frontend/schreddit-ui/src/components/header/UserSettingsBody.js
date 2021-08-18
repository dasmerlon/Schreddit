
import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import { Grid, Container, CssBaseline } from '@material-ui/core';

//"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MjkyODUxNzcsInN1YiI6InVpZDpkMDY2ZmIzNGUxOTY0NTI4YmYyMDc0ZDFlN2E2MTZlOCJ9.sVrTQtnB9O_lVUZOGw0zGgRjOgdRk96v0ygK_oPhfBI",
//"token_type": "bearer"


const useStyles = makeStyles((theme) => ({
    root: {
        backgroundColor: "#dae0e6",
        flexGrow: 1,
    },
    grid: {
        width: '100%',
        margin: '0px',
    },
    tabs: {
        textransform: "none",
    },
}));



function TabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`full-width-tabpanel-${index}`}
            aria-labelledby={`full-width-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box p={3}>
                    <Typography>{children}</Typography>
                </Box>
            )}
        </div>
    );
}
  
TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.any.isRequired,
    value: PropTypes.any.isRequired,
};

function a11yProps(index) {
    return {
        id: `full-width-tab-${index}`,
        'aria-controls': `full-width-tabpanel-${index}`,
    };
}


export default function UserSettingsBody() {
    const classes = useStyles();

    const theme = useTheme();
    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };
  
    const handleChangeIndex = (index) => {
        setValue(index);
    };

    return (
    <div className={classes.root}> 
        <React.Fragment>
        <CssBaseline />
            <Container fixed >
                <Grid item container spacing={3} direction='column' className={classes.grid} >
                    <Grid item>
                        <Typography variant="h5">User settings</Typography>
                    </Grid>
                    <Grid item>
                        <AppBar position="static" color="default">
                            <Tabs
                                value={value}
                                onChange={handleChange}
                                indicatorColor="primary"
                                textColor="primary"
                                variant="fullWidth"
                                aria-label="full width tabs example"
                            >
                            <Tab style={{textTransform: 'none'}} label="Account" {...a11yProps(0)} />
                            <Tab style={{textTransform: 'none'}} label="Profile" {...a11yProps(1)} />
                            <Tab style={{textTransform: 'none'}} label="Safety & Privacy" {...a11yProps(2)} />
                            <Tab style={{textTransform: 'none'}} label="Feed Settings" {...a11yProps(3)} />
                            <Tab style={{textTransform: 'none'}} label="Notifications" {...a11yProps(4)} />
                            <Tab style={{textTransform: 'none'}} label="Subscriptions" {...a11yProps(5)} />
                            <Tab style={{textTransform: 'none'}} label="Chat & Messaging" {...a11yProps(6)} />
                            </Tabs>
                        </AppBar>
                        <TabPanel value={value} index={0} dir={theme.direction}>
                            <Grid container spacing={3} direction='column' className={classes.grid} >
                                <Grid item>
                                    <Typography variant="h5">Account settings</Typography>
                                </Grid>
                            </Grid>
                        </TabPanel>
                        <TabPanel value={value} index={1} dir={theme.direction}>
                            Item Two
                        </TabPanel>
                        <TabPanel value={value} index={2} dir={theme.direction}>
                            Item Three
                        </TabPanel>
                    </Grid>
                </Grid>
            </Container>
        </React.Fragment>
    </div>
    );
} 

