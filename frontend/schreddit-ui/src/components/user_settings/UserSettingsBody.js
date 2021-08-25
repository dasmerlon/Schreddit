
import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import { Grid, Container, CssBaseline } from '@material-ui/core';
import { Divider, Button } from '@material-ui/core';
import axios from 'axios';
import configData from '../config.json';
import ChangeMail from './ChangeMail';

//Für meinen privaten user a@b.com, a, a
//"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MjkyODUxNzcsInN1YiI6InVpZDpkMDY2ZmIzNGUxOTY0NTI4YmYyMDc0ZDFlN2E2MTZlOCJ9.sVrTQtnB9O_lVUZOGw0zGgRjOgdRk96v0ygK_oPhfBI",
//"token_type": "bearer"


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    grid: {
        width: '100%',
        margin: '0px',
    },
    mainGrid: {
        maxWidth: '750px',
        margin: '0px',
        flexGrow: 1,
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


export default function UserSettingsBody(props) {
    const classes = useStyles();

    const theme = useTheme();
    const [value, setValue] = React.useState(0);
    const [email, setEmail] = React.useState("a@g.com");
    const [error, setError] = React.useState("");
    const [onlyPassword, setOnlyPassword] = React.useState(true);
    const [newPasword, setNewPassword] = React.useState("a");

    // For the navigation tabs
    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    useEffect(() => {
        console.log(props.cookies)
        if(props.cookies.loggedIn) { //if(email !== "")?
            axios.get(configData.USER_API_URL + "/" + props.cookies.username)
            .then(userResponse => {
                setEmail(userResponse.data.email);
            })
            .catch(error => {
                setEmail("User information could not load... Please try again later.");
                console.log(error);
            })
        } else {
            setEmail("")
        }    
    }, [props.cookies]);


    //EmailChange does not need a password -> only a new Email!
    //PasswordChange does only needs the new Password (no Email)
    const sendUserSettingsUpdate = async (onlyPassword) => {
        axios.put(configData.USER_SETTINGS_API_URL, {
            password: newPasword,
            email: email,
        },
            {
                headers: {
                    Authorization: `Bearer ${props.cookies.token}`
                }
            }).then(response => {
                console.log(response)
                //history.push("/r/" + subreddit.name);
            }).catch(error => {
                if (error.response.status === 304) {
                    setError({ message: "Please enter a new email or password." });
                } else {
                    setError({ message: "Something went wrong, please try again later." });
                }
                console.log(error.response);
            })
    };

    // For email we need new email, but for password change, we can use either username or email
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
                        <AppBar position="static" color="transparent" elevation={0}>
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
                            <Divider/>
                        </AppBar>
                        <TabPanel value={value} index={0} dir={theme.direction}>
                            <Grid container spacing={4} direction='column' className={classes.mainGrid} >
                                <Grid item>
                                    <Typography variant="h5">Account settings</Typography>
                                </Grid>
                                <Grid item>
                                    <Typography style={{color:"gray"}} variant="subtitle2">ACCOUNT PREFRENCES</Typography>
                                    <Divider />
                                </Grid>
                                <Grid item>
                                    <Grid item container spacing={10} justifyContent="space-between">
                                        <Grid item>
                                            <Grid container spacing={0} direction='column'>
                                                <Grid item>
                                                    <Typography variant="h5" >Email address</Typography>
                                                </Grid>
                                                <Grid item>
                                                    <Typography variant="subtitle2" >{email}</Typography>
                                                </Grid>
                                            </Grid>
                                        </Grid>
                                        <Grid item>
                                            <ChangeMail 
                                                cookies={props.cookies}
                                            />
                                        </Grid>
                                    </Grid>
                                    <Grid item container spacing={10} justifyContent="space-between">
                                        <Grid item>
                                            <Grid container spacing={0} direction='column'>
                                                <Grid item>
                                                    <Typography variant="h5" >Change password</Typography>
                                                </Grid>
                                                <Grid item>
                                                    <Typography variant="subtitle2" >Password must be at least 8 characters long</Typography>
                                                </Grid>
                                            </Grid>
                                        </Grid>
                                        <Grid item>
                                            <Button variant="outlined" color="primary" onClick={sendUserSettingsUpdate} style={{textTransform:"none"}}>Change</Button>
                                        </Grid>
                                    </Grid>
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
