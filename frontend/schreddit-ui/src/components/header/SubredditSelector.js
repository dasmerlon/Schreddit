import React from 'react';
import { useHistory } from "react-router-dom"
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import AddIcon from '@material-ui/icons/Add';
import ImageIcon from '@material-ui/icons/Image';
import HomeIcon from '@material-ui/icons/Home';
import DropDownArrowIcon from '@material-ui/icons/ArrowDropDown'

const StyledButton = withStyles({
    contained: {
        backgroundColor: 'white',
        color: 'grey',
        border: '2px solid grey',
        boxShadow: 'none',
        marginLeft: '15px',
        height: '39px'
    },
})(Button);

const StyledMenu = withStyles({
    paper: {
        border: '1px solid #d3d4d5',
    },
})((props) => (
    <Menu
        elevation={0}
        getContentAnchorEl={null}
        anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'center',
        }}
        transformOrigin={{
            vertical: 'top',
            horizontal: 'center',
        }}
        {...props}
    />
));

const StyledMenuItem = withStyles((theme) => ({
    root: {
        '&:focus': {
            backgroundColor: theme.palette.common.grey,
            '& .MuiListItemIcon-root, & .MuiListItemText-primary': {
                color: theme.palette.common.grey,
            },
        },
    },
}))(MenuItem);


export default function Dropdown(props) {
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
        console.log(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const [subreddit, setSubreddit] = React.useState('Open Menu');

    let history = useHistory();
    const handleChange = (event) => {
        if (event.target.innerText === "Create Subreddit") {
            history.push("/CreateSubreddit");
        }
        else if (event.target.innerText === "Home") {
            history.push("/");
        }
        handleClose();
        setSubreddit(event.target.innerText);
        console.log(event.target.innerText);
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
                <StyledButton
                    aria-controls="customized-menu"
                    aria-haspopup="true"
                    variant="contained"
                    onClick={handleClick}
                >
                    {subreddit}
                    <DropDownArrowIcon />
                </StyledButton>
                <StyledMenu
                    id="customized-menu"
                    anchorEl={anchorEl}
                    keepMounted
                    open={Boolean(anchorEl)}
                    onClose={handleClose}
                >
                    <StyledMenuItem onClick={handleChange}>
                        <ListItemIcon>
                            <HomeIcon fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary="Home" />
                    </StyledMenuItem>
                    <StyledMenuItem onClick={handleChange}>
                        <ListItemIcon>
                            <AddIcon fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary="Create Subreddit" />
                    </StyledMenuItem>
                    <StyledMenuItem onClick={handleChange}>
                        <ListItemIcon>
                            <ImageIcon fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary="Subreddit1" />
                    </StyledMenuItem>
                </StyledMenu>
            </div>
        );
    }
}
