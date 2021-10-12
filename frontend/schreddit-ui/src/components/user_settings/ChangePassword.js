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


export default function ChangePassword(props) {
    const [showPasswordChangeDialog, setShowPasswordChangeDialog] = React.useState(false);
    const [password, setPassword] = React.useState("");
    const [passwordConfirmed, setPasswordConfirmed] = React.useState("");
    const [error, setError] = React.useState("");

    const openPasswordChangeDialog = () => {
        setError({ message: "" })
        setShowPasswordChangeDialog(true);
    };

    const handlePasswordChangeDialogClose = () => {
        setShowPasswordChangeDialog(false);
    };

    const handlePasswordChange = (independentPassword, event) => {
        if(independentPassword == passwordConfirmed){
            if(password.password === passwordConfirmed.password) {      
                setPasswordConfirmed({
                    password: event.target.value,
                    errorMessage: "",
                    error: false
                });    
            } else {
                setPasswordConfirmed({
                    password: event.target.value,
                    errorMessage: "Password must match",
                    error: true
                });              
            }
        } else {
            setPassword({
                password: event.target.value
            }); 

            if(password.password === passwordConfirmed.password) {      
                setPasswordConfirmed({
                    password: passwordConfirmed.password,
                    errorMessage: "",
                    error: false
                });    
            } else {
                setPasswordConfirmed({
                    password: passwordConfirmed.password,
                    errorMessage: "Password must match",
                    error: true
                });              
            }
        }
    }

    const sendUserSettingsUpdate = async () => {
        axios.put(configData.USER_API_URL, {
            password: password.password
        },
            {
                headers: {
                    Authorization: `Bearer ${props.cookies.token}`
                }
            }).then(response => {
                console.log(response)
                handlePasswordChangeDialogClose();
                window.location.reload();
                //history.push("/r/" + subreddit.name);
            }).catch(error => {
                if (error.response.status === 304) {
                    setError({ message: "Please enter a new password." });
                } 
                else if (error.response.status === 401) {
                    props.handleLogout();
                    props.setShowLogin(true);
                }
                else {
                    setError({ message: "Something went wrong, please try again later." });
                }
                console.log(error.response);
            })
    };

    return (
        <div>
            <Button variant="outlined" aria-label="change password button" style={{ margin: '7px' }} color="inherit" onClick={openPasswordChangeDialog}>
                Change
                        </Button>
            <Dialog open={showPasswordChangeDialog} onClose={handlePasswordChangeDialogClose} onKeyDown={(e) => { if (e.keyCode === 13) { sendUserSettingsUpdate() } }} aria-labelledby="change-password-form-dialog">
                <DialogTitle id="change-password-form-dialog-title">Change Password</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Please provide your new password to login to Schreddit in the future:
                                </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="password"
                        label="New Password"
                        type="password"
                        helperText={password.errorMessage}
                        variant="outlined"
                        error={password.error}
                        fullWidth
                        onChange={(e) => handlePasswordChange(password, e)}
                        onBlur={(e) => handlePasswordChange(password, e)}
                    />
                    <TextField
                        margin="dense"
                        id="passwordConfirmed"
                        label="Confirm New Password"
                        type="password"
                        helperText={passwordConfirmed.errorMessage}
                        variant="outlined"
                        error={passwordConfirmed.error}
                        fullWidth
                        onChange={(e) => handlePasswordChange(passwordConfirmed, e)}
                        onBlur={(e) => handlePasswordChange(passwordConfirmed, e)}
                    />
                    <p >
                        {error.message}
                    </p>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handlePasswordChangeDialogClose} color="primary">
                        Cancel
                                </Button>
                    <Button onClick={sendUserSettingsUpdate} color="primary">
                        Save password
                                </Button>
                </DialogActions>
            </Dialog>
        </div>
    )
}