import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));

export default function Dropdown(props) {
    const classes = useStyles();
    const [subreddit, setSubreddit] = React.useState('');

    const handleChange = (event) => {
        setSubreddit(event.target.value);
    };


    if (!props.cookies.loggedIn) {
        return (
            <div>

            </div>
        )
    }
    else {
        return (
            <div>
                <FormControl variant="outlined" className={classes.formControl}>
                    <InputLabel id="subreddit-selector-label">Home</InputLabel>
                    <Select
                        labelId="subreddit-selector-label"
                        id="subreddit-selector"
                        value={subreddit}
                        onChange={handleChange}
                        label="Subreddits"
                    >
                        <MenuItem value="create-subreddit">Create Subreddit</MenuItem>
                        <MenuItem value={10}>Dummy01</MenuItem>
                        <MenuItem value={20}>Dummy02</MenuItem>
                        <MenuItem value={30}>Dummy03</MenuItem>
                    </Select>
                </FormControl>
            </div>
        )
    }
}
