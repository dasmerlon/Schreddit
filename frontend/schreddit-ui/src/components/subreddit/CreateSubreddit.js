import React from 'react';
import TextField from '@material-ui/core/TextField';
import InputAdornment from '@material-ui/core/InputAdornment';
import Button from '@material-ui/core/Button';
import configData from '../config.json'
import axios from 'axios';
import MenuItem from '@material-ui/core/MenuItem';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import { useHistory } from "react-router-dom"
import { makeStyles } from "@material-ui/core/styles";


const useStyles = makeStyles((theme) => ({
    container: {
        width: '70%',
        margin: 'auto',
        paddingTop: '10px'
    },
    textField: {
        marginBottom: '10px'
    },
    formControl: {
        width: '100%'
    },
    submitButton:  {
        backgroundColor: 'white',
        color: 'grey',
        border: '1px solid grey',
        boxShadow: 'none',
        marginTop: '10px',
        height: '39px'
    }
}));

export default function CreateSubreddit(props) {
    const classes = useStyles();
    let history = useHistory();
    const [subreddit, setSubreddit] = React.useState({
        name: '',
        title: '',
        description: '',
        type: ''
    });

    const [error, setError] = React.useState("");

    const handleSubredditNameChange = event => {
        setSubreddit({
            name: event.target.value,
            title: subreddit.title,
            description: subreddit.description,
            type: subreddit.type
        })
    };

    const handleSubredditTitleChange = event => {
        setSubreddit({
            name: subreddit.name,
            title: event.target.value,
            description: subreddit.description,
            type: subreddit.type
        })
    };

    const handleSubredditDescriptionChange = event => {
        setSubreddit({
            name: subreddit.name,
            title: subreddit.title,
            description: event.target.value,
            type: subreddit.type
        })
    };

    const handleSubredditTypeChange = event => {
        setSubreddit({
            name: subreddit.name,
            title: subreddit.title,
            description: subreddit.description,
            type: event.target.value
        })
    };

    const sendCreateSubredditData = async () => {
        axios.post(configData.SUBREDDIT_API_URL + subreddit.name, {
            sr: subreddit.name,
            title: subreddit.title,
            description: subreddit.description,
            type: subreddit.type
        },
            {
                headers: {
                    Authorization: `Bearer ${props.cookies.token}`
                }
            }).then(response => {
                history.push("/r/" + subreddit.name);
            }).catch(error => {
                console.log(error.response)
                if (error.response.status === 422) {
                    setError({ message: "Please check your input. Something is not valid." });
                } 
                else if (error.response.status === 401){
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
        <div className={classes.container}>
            <form onSubmit={sendCreateSubredditData}>
                <TextField
                    name="subredditName"
                    variant="outlined"
                    required
                    fullWidth
                    className={classes.textField}
                    InputProps={{
                        startAdornment: <InputAdornment position="start">r/ </InputAdornment>,
                    }}
                    id="subredditName"
                    label="Subreddit Name"
                    onChange={handleSubredditNameChange}
                    autoFocus
                />
                <TextField
                    name="subredditTitle"
                    variant="outlined"
                    required
                    fullWidth
                    className={classes.textField}
                    id="subredditTitle"
                    label="Subreddit Title"
                    onChange={handleSubredditTitleChange}
                />
                <TextField
                    id="subredditDescription"
                    name="description"
                    label="Description"
                    required
                    multiline
                    rows={4}
                    fullWidth
                    className={classes.textField}
                    variant="outlined"
                    onChange={handleSubredditDescriptionChange}
                />
                <FormControl variant="outlined" className={classes.formControl}>
                    <InputLabel id="subreddit-type-dropdown-label">Type</InputLabel>
                    <Select
                        required
                        labelId="subreddit-type-dropdown-label"
                        id="subreddit-type-dropdown"
                        onChange={handleSubredditTypeChange}
                        label="Type"
                    >
                        <MenuItem value={'public'}>Public</MenuItem>
                        <MenuItem value={'private'}>Private</MenuItem>
                        <MenuItem value={'restricted'}>Restricted</MenuItem>
                    </Select>
                </FormControl>
                <label style={{ color: 'red' }}>{error.message}</label>
                <br />
                <Button type="submit" className={classes.submitButton}>
                    Create Subreddit
                </Button>
            </form>
        </div >
    )
}
