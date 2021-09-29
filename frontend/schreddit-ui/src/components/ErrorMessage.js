import * as React from 'react';
import Snackbar from "@material-ui/core/Snackbar";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";


export default function ErrorMessage(props) {
    const [open, setOpen] = React.useState(true);

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setOpen(false);
        if(status === 401 && props.cookies.loggedIn){
            props.handleLogout();
            props.setShowLogin(true);
            console.log('yayeet')
        }
        console.log('yayeet2');
        props.setError('');
    };

    const action = (
        <React.Fragment>
            <IconButton
                size="small"
                aria-label="close"
                color="inherit"
                onClick={handleClose}
            >
                <CloseIcon fontSize="small" />
            </IconButton>
        </React.Fragment>
    );

    // determine status code
    let status;
    if (props.error.response) {
        status = props.error.response.status;
    }
    else if (props.error.request) {
        status = 0;
    }
    else {
        status = -1;
    }

    // set error message
    let errorMessage;
    if (status === 422) {
        errorMessage = props.error.response.data.detail[0].msg
    }
    else if (status === 304) {
        errorMessage = "The resource remains unchanged."
    }
    else if (status === 401) {
        if (props.cookies.loggedIn){
            errorMessage = "Your session timed out, please login again."
        }
        else {
            errorMessage = "To perform this action, you need to be logged in."
        }
    }
    else if (status >= 400 && status < 500) {
        errorMessage = props.error.response.data.detail
    }
    else if (status === 500) {
        errorMessage = "Internal Server Error"
    }
    else if (status === 0) {
        errorMessage = "The request was sent, but no response from the server was received."
    }
    else if (status === -1) {
        errorMessage = "There was an error while setting up the request."
    }

    return (
        <Snackbar
            open={open}
            autoHideDuration={4500}
            onClose={handleClose}
            message={errorMessage}
            action={action}
        />
    );
}
