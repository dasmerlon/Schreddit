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
import ErrorMessage from "../ErrorMessage";


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
    const [sr, setSr] = React.useState('')
    const [title, setTitle] = React.useState('')
    const [description, setDescription] = React.useState('')
    const [type, setType] = React.useState('')

    const [error, setError] = React.useState("");

    const handleSrChange = event => {
        setSr(event.target.value)
    };

    const handleTitleChange = event => {
        setTitle(event.target.value)
    };

    const handleDescriptionChange = event => {
        setDescription(event.target.value)
    };

    const handleTypeChange = event => {
        setType(event.target.value)
    };

    const handleSubmit = async (event) => {
        axios.post(configData.SUBREDDIT_API_URL, {
            sr: sr,
            title: title,
            description: description,
            type: type
        },
        {
            headers: {
                Authorization: `Bearer ${props.cookies.token}`
            }
        }).then(response => {
            history.push("/r/" + response.data.sr);
        }).catch(error => {
            console.log(error)
            setError(error)
        });
        event.preventDefault()
    };

    return (
        <div className={classes.container}>
            { error !== '' &&
            <ErrorMessage error={error} setError={setError} cookies={props.cookies} setShowLogin={props.setShowLogin}/>
            }
            <form onSubmit={handleSubmit}>
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
                    onChange={handleSrChange}
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
                    onChange={handleTitleChange}
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
                    onChange={handleDescriptionChange}
                />
                <FormControl variant="outlined" className={classes.formControl}>
                    <InputLabel id="subreddit-type-dropdown-label">Type</InputLabel>
                    <Select
                        required
                        labelId="subreddit-type-dropdown-label"
                        id="subreddit-type-dropdown"
                        value={type}
                        onChange={handleTypeChange}
                        label="Type"
                    >
                        <MenuItem value={'public'}>Public</MenuItem>
                        <MenuItem value={'private'}>Private</MenuItem>
                        <MenuItem value={'restricted'}>Restricted</MenuItem>
                    </Select>
                </FormControl>
                <br />
                <Button type="submit" className={classes.submitButton}>
                    Create Subreddit
                </Button>
            </form>
        </div >
    )
}
