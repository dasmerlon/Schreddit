import React from 'react';
import configData from '../config.json'
import axios from 'axios';
import Button from '@material-ui/core/Button'
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';


export default function Login(props) {
    const [showLoginDialog, setShowLoginDialog] = React.useState(false);

    const openLoginDialog = () => {
        props.setError({ message: "" })
        setShowLoginDialog(true);
    };

    const handleLoginDialogClose = () => {
        setShowLoginDialog(false);
    };

    const sendLoginData = async () => {
        const loginData = new URLSearchParams();
        loginData.append('username', props.email.email);
        loginData.append('password', props.password.password);
        axios.post(configData.LOGIN_API_URL, loginData)
            .then(response => {
                const token = response.data.access_token;

                axios.get(configData.USER_API_URL + "/" + props.email.email)
                    .then(userResponse => {
                        props.handleLogin(token, userResponse.data.username);
                        handleLoginDialogClose();
                    })
                    .catch(error => {
                        props.setError({ message: "User information could not load... Please try again later." });
                        console.log(error);
                    });
            })
            .catch(error => {
                props.setError({ message: "Something went wrong, please try again later." });
                console.log(error);
            });
    };

    if (!props.cookies.loggedIn) {
            return (
                <div>
                    <Button variant="outlined" aria-label="login button" style={{ margin: '7px' }} color="inherit" onClick={openLoginDialog}>
                        Login
                                </Button>
                    <Dialog open={showLoginDialog} onClose={handleLoginDialogClose} onKeyDown={(e) => { if (e.keyCode === 13) { sendLoginData() } }} aria-labelledby="login-form-dialog">
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
                            <p >
                                {props.error.message}
                            </p>
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
                    <Button variant="outlined" aria-label="login button" style={{ margin: '7px' }} color="inherit" onClick={props.handleLogout}>
                        Logout
                    </Button>
                </div>
            )
        }

}