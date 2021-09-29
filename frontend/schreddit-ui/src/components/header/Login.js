import React, { useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import configData from '../config.json'
import axios from 'axios';
import Button from '@material-ui/core/Button'
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { CardActionArea, Grid, Typography } from '@material-ui/core';
import AccountCircle from '@material-ui/icons/AccountCircle';
import { Avatar } from '@material-ui/core';
import ErrorMessage from "../ErrorMessage";

const useStyles = makeStyles((theme) => ({
    small: {
        width: theme.spacing(3),
        height: theme.spacing(3),
    },
    username: {
        paddingTop: 10,
    }
}));


export default function Login(props) {
    const classes = useStyles();

    const [renderProfile, setrenderProfile] = React.useState(null);
    const [error, setError] = React.useState('');

    const openLoginDialog = () => {
        props.setShowLogin(true);
    };

    const handleLoginDialogClose = () => {
        props.setShowLogin(false);
    };

    const sendLoginData = async () => {
        const loginData = new URLSearchParams();
        loginData.append('username', props.email.email);
        loginData.append('password', props.password.password);
        axios.post(configData.LOGIN_API_URL, loginData)
            .then(response => {
                const token = response.data.access_token;

                axios.get(configData.USER_API_URL + "/u/" + props.email.email)
                    .then(userResponse => {
                        props.handleLogin(token, userResponse.data.username);
                        handleLoginDialogClose();
                    })
                    .catch(error => {
                        setError(error);
                    });
            })
            .catch(error => {
                setError(error)
            });
    };

    useEffect(() => {
        if(props.cookies.loggedIn) { 
            setrenderProfile ("/settings/account")
        } else {
            setrenderProfile("/")
        }    
    }, [props.cookies.loggedIn]);

    if (!props.cookies.loggedIn) {
            return (
                <div>
                    { error !== '' &&
                    <ErrorMessage error={error} setError={setError} cookies={props.cookies}/>
                    }
                    <Button variant="outlined" aria-label="login button" style={{ margin: '7px' }} color="inherit" onClick={openLoginDialog}>
                        Login
                                </Button>
                    <Dialog open={props.showLogin} onClose={handleLoginDialogClose} onKeyDown={(e) => { if (e.keyCode === 13) { sendLoginData() } }} aria-labelledby="login-form-dialog">
                        <DialogTitle id="login-form-dialog-title">Login</DialogTitle>
                        <DialogContent>
                            <DialogContentText>
                                Please provide your username or email address and your password to login to Schreddit:
                                        </DialogContentText>
                            <TextField
                                autoFocus
                                margin="dense"
                                id="email"
                                label="Username / Email Address"
                                type="email"
                                helperText={props.email.errorMessage}
                                variant="outlined"
                                error={props.email.error}
                                fullWidth
                                onChange={props.handleEmailChange}
                                onBlur={props.handleEmailChange}
                            />
                            <TextField
                                margin="dense"
                                id="password"
                                label="Password"
                                type="password"
                                variant="outlined"
                                fullWidth
                                onChange={props.handlePasswordChange}
                            />
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={handleLoginDialogClose} color="primary">
                                Cancel
                            </Button>
                            <Button onClick={sendLoginData} color="primary">
                                Login
                            </Button>
                        </DialogActions>
                    </Dialog>
                </div>
            )
        } else {
            return (
                <div>
                    <Grid container spacing={1}> 
                        <Grid item>
                            <Button variant="outlined" aria-label="login button" style={{ margin: '7px' }} color="inherit" onClick={props.handleLogout}>
                                Logout
                            </Button>
                        </Grid>
                        <Grid item>
                            <CardActionArea href={renderProfile} >
                                <div className={classes.username}>
                                    <Grid container direction="row" spacing={1}>
                                        <Grid item >
                                            <Avatar className={classes.small}>
                                                <AccountCircle />
                                            </Avatar>
                                        </Grid>
                                        <Grid item>
                                            <Typography variant="h6" noWrap>
                                                {props.cookies.username}
                                            </Typography>
                                        </Grid>
                                    </Grid>
                                </div>
                            </CardActionArea>
                        </Grid>
                    </Grid>
                </div>
            )
        }

}