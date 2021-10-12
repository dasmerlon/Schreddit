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


export default function ChangeMail(props) {
    const [showEmailChangeDialog, setShowEmailChangeDialog] = React.useState(false);
    const [email, setEmail] = React.useState("");
    const [emailConfirmed, setEmailConfirmed] = React.useState("");
    const [error, setError] = React.useState("");

    const openEmailChangeDialog = () => {
        setError({ message: "" })
        setShowEmailChangeDialog(true);
    };

    const handleEmailChangeDialogClose = () => {
        setShowEmailChangeDialog(false);
    };

    const handleEmailChange = (setIndependentEmail, independentEmail, event) => {
        const temp = "";
        if (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(independentEmail.email)) {
            setIndependentEmail({
                email: event.target.value,
                errorMessage: "",
                error: false
            });

        } else {
            setIndependentEmail({
                email: event.target.value,
                errorMessage: "The email is not valid",
                error: true
            });
            const temp = "The email is not valid";
        }

        if(independentEmail == emailConfirmed){
            if(email.email === emailConfirmed.email) {      
                setEmailConfirmed({
                    email: event.target.value,
                    errorMessage: "" + temp,
                    error: false
                });    
            } else {
                setEmailConfirmed({
                    email: event.target.value,
                    errorMessage: "Email must match",
                    error: true
                });              
            }
        } else {
            if(email.email === emailConfirmed.email) {      
                setEmailConfirmed({
                    email: emailConfirmed.email,
                    errorMessage: "" + emailConfirmed.errorMessage,
                    error: false
                });    
            } else {
                setEmailConfirmed({
                    email: emailConfirmed.email,
                    errorMessage: "Email must match",
                    error: true
                });              
            }
        }
    }

    const sendUserSettingsUpdate = async () => {
        if(emailConfirmed.email === email.email) {
            axios.put(configData.USER_API_URL, {
                email: email.email
            },
            {
                headers: {
                    Authorization: `Bearer ${props.cookies.token}`
                }
            }).then(response => {
                handleEmailChangeDialogClose();
                window.location.reload();
                //history.push("/r/" + subreddit.name);
            }).catch(error => {
                if (error.response.status === 304) {
                    setError({ message: "Please enter a new email." });
                }
                else if (error.response.status === 401) {
                    props.handleLogout();
                    props.setShowLogin(true);
                } 
                else {
                    setError({ message: "Something went wrong, please try again later." });
                }
            })
        } else {
            setError({ message: "The emails have to match." });
        }
    };

    return (
        <div>
            <Button variant="outlined" aria-label="change email button" style={{ margin: '7px' }} color="inherit" onClick={openEmailChangeDialog}>
                Change
                        </Button>
            <Dialog open={showEmailChangeDialog} onClose={handleEmailChangeDialogClose} onKeyDown={(e) => { if (e.keyCode === 13) { sendUserSettingsUpdate() } }} aria-labelledby="change-email-form-dialog">
                <DialogTitle id="change-email-form-dialog-title">Change Email</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Please provide your new email address to login to Schreddit in the future:
                    </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="email"
                        label="New Email Address"
                        type="email"
                        helperText={email.errorMessage}
                        variant="outlined"
                        error={email.error}
                        fullWidth
                        onChange={(e) => handleEmailChange(setEmail, email, e)}
                        onBlur={(e) => handleEmailChange(setEmail, email, e)}
                    />
                    <TextField
                        margin="dense"
                        id="emailConfirmed"
                        label="Confirm New Email Address"
                        type="email"
                        helperText={emailConfirmed.errorMessage}
                        variant="outlined"
                        error={emailConfirmed.error}
                        fullWidth
                        onChange={(e) => handleEmailChange(setEmailConfirmed, emailConfirmed, e)}
                        onBlur={(e) => handleEmailChange(setEmailConfirmed, emailConfirmed, e)}
                    />
                    <p >
                        {error.message}
                    </p>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleEmailChangeDialogClose} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={sendUserSettingsUpdate} color="primary">
                        Save email
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    )
}