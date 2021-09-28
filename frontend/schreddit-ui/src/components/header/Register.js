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
import { InputAdornment } from '@material-ui/core';
import ErrorMessage from "../ErrorMessage";

export default function Register(props) {
    const [showRegisterDialog, setShowRegisterDialog] = React.useState(false);
    const [titleValue, setTitleValue] = React.useState('');
    const [error, setError] = React.useState('');

    const handleTitleChange = (event) => {
      setTitleValue(event.target.value);
    };

    const openRegisterDialog = () => {
        setShowRegisterDialog(true);
    };

    const handleRegisterDialogClose = () => {
        setShowRegisterDialog(false);
    };


    const sendRegisterData = async () => {
        axios.post(configData.USER_API_URL + '/register', {
            email: props.email.email,
            username: props.username.username,
            password: props.password.password
        }).then(response => {
            handleRegisterDialogClose();
        }).catch(error => {
            setError(error)
        })
    };
    if (!props.cookies.loggedIn) {
        return (
            <div>
                { error !== '' &&
                <ErrorMessage error={error} setError={setError}/>
                }
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
                            variant="outlined"
                            error={props.email.error}
                            helperText={props.email.errorMessage}
                            fullWidth
                            onInput={props.handleEmailChange}
                            onBlur={props.handleEmailChange}
                        />
                        <TextField
                            margin="dense"
                            id="username"
                            label="Username"
                            type="text"
                            variant="outlined"
                            error={props.username.error}
                            helperText={props.username.errorMessage}
                            fullWidth
                            onInput={props.handleUsernameChange}
                            onBlur={props.handleUsernameChange}
                            onChange={handleTitleChange}
                            InputProps={{
                                endAdornment: <InputAdornment position="end">{titleValue.length}/17</InputAdornment>
                            }}
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
    } else {
        return (
            <div>

            </div>
        )
    }
}