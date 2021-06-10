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


export default function Register(props) {
    const [showRegisterDialog, setShowRegisterDialog] = React.useState(false);

    const openRegisterDialog = () => {
        setShowRegisterDialog(true);
    };

    const handleRegisterDialogClose = () => {
        setShowRegisterDialog(false);
    };


    const sendRegisterData = async () => {
        const response = await axios.post(configData.USER_API_URL + '/register', {
            email: props.email.email,
            username: props.username.username,
            password: props.password.password
        })
        handleRegisterDialogClose();
    };

    return (
        <div>
            <Button variant="outlined" aria-label="register button" style={{ margin: '7px' }} color="inherit" styles="theme.spacing(1)" onClick={openRegisterDialog}>
                Register
                            </Button>
            <Dialog open={showRegisterDialog} onClose={handleRegisterDialogClose} onKeyDown={(e) => { if (e.keyCode === 13) { sendRegisterData() } }} aria-labelledby="register-form-dialog">
                <DialogTitle id="register-form-dialog-title">Register</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        To register to schreddit please enter the following information:
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
                        id="username"
                        label="Username"
                        type="text"
                        fullWidth
                        onChange={props.handleUsernameChange}
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
                    <Button onClick={handleRegisterDialogClose} color="primary">
                        Cancel
                                </Button>
                    <Button onClick={sendRegisterData} color="primary">
                        Register
                                </Button>
                </DialogActions>
            </Dialog>

        </div>
    )

}