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
        setShowLoginDialog(true);
    };

    const handleLoginDialogClose = () => {
        setShowLoginDialog(false);
    };

    const sendLoginData = async () => {
        const loginData = new URLSearchParams();
        loginData.append('username', props.email.email);
        loginData.append('password', props.password.password);
        const response = await axios.post(configData.LOGIN_API_URL, loginData);
        props.handleLogin(response.data.access_token);
        handleLoginDialogClose();
    };

    return (
        <div>
            <Button variant="outlined" aria-label="login button" style={{ margin: '7px' }} color="inherit" onClick={openLoginDialog}>
                Login
                        </Button>
            <Dialog open={showLoginDialog} onClose={handleLoginDialogClose} onKeyDown={(e) => { if (e.keyCode === 13) { sendLoginData() } }} aria-labelledby="login-form-dialog">
                <DialogTitle id="login-form-dialog-title">Login</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Please provide your username and your password to login to Schreddit:
                                </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="Email Address"
                        type="email"
                        fullWidth
                        onChange={props.handleEmailChange}
                    />
                    <TextField
                        margin="dense"
                        id="password"
                        label="Password"
                        type="password"
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

}