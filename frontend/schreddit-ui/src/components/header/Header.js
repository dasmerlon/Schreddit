import React from 'react';
import { fade, makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import InputBase from '@material-ui/core/InputBase';
import Badge from '@material-ui/core/Badge';
import MenuItem from '@material-ui/core/MenuItem';
import Menu from '@material-ui/core/Menu';
import SearchIcon from '@material-ui/icons/Search';
import AccountCircle from '@material-ui/icons/AccountCircle';
import MailIcon from '@material-ui/icons/Mail';
import NotificationsIcon from '@material-ui/icons/Notifications';
import MoreIcon from '@material-ui/icons/MoreVert';
import Login from './Login'
import Register from './Register'
import Dropdown from './SubredditSelector'
import Logo from '../../images/schreddit.svg'
import { CardActionArea, Dialog, DialogTitle, List, ListItem, ListItemAvatar, Avatar, ListItemText } from '@material-ui/core';
import axios from 'axios';
import configData from '../config.json';
import ErrorMessage from '../ErrorMessage';
import { useHistory } from 'react-router';

const useStyles = makeStyles((theme) => ({
    grow: {
        flexGrow: 1,
    },

    appBar: {
        backgroundColor: 'white',
        color: 'grey'
    },

    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        display: 'none',
        [theme.breakpoints.up('sm')]: {
            display: 'block',
        },
    },
    schredditIcon: {
        width: '3%',
        paddingRight: '10px'
    },
    search: {
        position: 'relative',
        borderRadius: theme.shape.borderRadius,
        backgroundColor: fade(theme.palette.common.white, 0.15),
        '&:hover': {
            backgroundColor: fade(theme.palette.common.white, 0.25),
        },
        marginRight: theme.spacing(2),
        marginLeft: 0,
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            marginLeft: '5.5%',
            width: '40%',
            borderStyle: 'solid',
            border: '2px   '
        },
    },
    searchIcon: {
        padding: theme.spacing(0, 2),
        height: '100%',
        position: 'absolute',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputRoot: {
        color: 'inherit',
        display: 'block',
    },
    inputInput: {
        padding: theme.spacing(1, 1, 1, 0),
        // vertical padding + font size from searchIcon
        paddingLeft: `calc(1em + ${theme.spacing(4)}px)`,
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('md')]: {
            width: '20ch',
        },
    },
    sectionDesktop: {
        display: 'none',
        marginInlineEnd: "4%",
        [theme.breakpoints.up('md')]: {
            display: 'flex',
        },
    },
    sectionMobile: {
        display: 'flex',
        [theme.breakpoints.up('md')]: {
            display: 'none',
        },
    },
    logo: {
        width: 90,
    },
}));



export default function PrimarySearchAppBar(props) {
    const classes = useStyles();
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [mobileMoreAnchorEl, setMobileMoreAnchorEl] = React.useState(null);

    const isMenuOpen = Boolean(anchorEl);
    const isMobileMenuOpen = Boolean(mobileMoreAnchorEl);

    const handleProfileMenuOpen = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleMobileMenuClose = () => {
        setMobileMoreAnchorEl(null);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
        handleMobileMenuClose();
    };

    const handleMobileMenuOpen = (event) => {
        setMobileMoreAnchorEl(event.currentTarget);
    };




    const [error, setError] = React.useState("");
    const [username, setUsername] = React.useState("");
    const [email, setEmail] = React.useState("");
    const [password, setPassword] = React.useState("");

    const handleEmailChange = event => {
        if(event.target.value.includes('@')){
            if (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(event.target.value)) {
                setEmail({
                    email: event.target.value,
                    errorMessage: "",
                    error: false
                });
    
            } else {
                setEmail({
                    email: event.target.value,
                    errorMessage: "The email is not valid",
                    error: true
                });
            }
        }
        else {
            setEmail({
                email: event.target.value,
                errorMessage: "",
                error: false
            });
        }
    }
    
    const handleUsernameChange = event => {
        if (/^[\wöüßä]{1,17}$/.test(username.username)) {
            setUsername({
                username: event.target.value,
                errorMessage: "",
                error: false
            });

        } else {
            setUsername({
                username: event.target.value,
                errorMessage: "The username is not valid (no symbols and 1-17 characters).",
                error: true
            });
        }
    }

    const handlePasswordChange = event => {
        setPassword({
            password: event.target.value,
        })
    }




    const menuId = 'primary-search-account-menu';
    const renderMenu = (
        <Menu
            anchorEl={anchorEl}
            anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            id={menuId}
            keepMounted
            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            open={isMenuOpen}
            onClose={handleMenuClose}
        >
            <MenuItem onClick={handleMenuClose}>Profile</MenuItem>
            <MenuItem onClick={handleMenuClose}>My account</MenuItem>
        </Menu>
    );

    //TODO: Edit mobile view
    const mobileMenuId = 'primary-search-account-menu-mobile';
    const renderMobileMenu = (
        <Menu
            anchorEl={mobileMoreAnchorEl}
            anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            id={mobileMenuId}
            keepMounted
            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            open={isMobileMenuOpen}
            onClose={handleMobileMenuClose}
        >
            <MenuItem>
                <IconButton aria-label="show 4 new mails" color="inherit">
                    <Badge badgeContent={4} color="secondary">
                        <MailIcon />
                    </Badge>
                </IconButton>
                <p>Messages</p>
            </MenuItem>
            <MenuItem>
                <IconButton aria-label="show 11 new notifications" color="inherit">
                    <Badge badgeContent={11} color="secondary">
                        <NotificationsIcon />
                    </Badge>
                </IconButton>
                <p>Notifications</p>
            </MenuItem>
            <MenuItem onClick={handleProfileMenuOpen}>
                <IconButton
                    aria-label="account of current user"
                    aria-controls="primary-search-account-menu"
                    aria-haspopup="true"
                    color="inherit"
                >
                    <AccountCircle />
                </IconButton>
                <p>Profile</p>
            </MenuItem>
        </Menu>
    );


    const [dialog, setDialog] = React.useState("");

    const handleSearchBarChange = (event) => {
        if(event.key === 'Enter'){
            searchFor(event.target.value);
        } 
    };

    function searchFor(sr) {
        axios.get(configData.SEARCH_API_URL, {
            params: {
                q: sr,
                include_title: true
            }
        }
        ).then(response => {
            setDialog(<SearchResultsDialog handleClose={handleClose} open={true} searchBarResults={response.data} />)
        }).catch(error => {
            console.log(error)
            setError(error)
        });
    }

    function handleClose() {
        setDialog("");
    };
  

    return (
        <div className={classes.grow}>
            { error !== '' &&
            <ErrorMessage error={error} setError={setError} cookies={props.cookies} setShowLogin={props.setShowLogin}/>
            }
            <AppBar position="static" className={classes.appBar}>
                <Toolbar>
                    <img alt="" src={Logo} className={classes.schredditIcon} />
                    <CardActionArea href="/" className={classes.logo}>
                        <Typography className={classes.title} variant="h6" noWrap>
                            Schreddit
                        </Typography>
                    </CardActionArea>
                    <Dropdown
                        cookies={props.cookies}
                    />
                    <div className={classes.search}>
                        <div className={classes.searchIcon}>
                            <SearchIcon />
                        </div>
                            <InputBase
                                placeholder="Search…"
                                classes={{
                                    root: classes.inputRoot,
                                    input: classes.inputInput,
                                }}
                                inputProps={{ 'aria-label': 'search' }}
                                onKeyPress={handleSearchBarChange}
                            />
                        </div>
                    <div className={classes.grow} />
                    <div className={classes.sectionDesktop}>
                        <Login
                            email={email}
                            password={password}
                            handleEmailChange={handleEmailChange}
                            handlePasswordChange={handlePasswordChange}
                            handleLogin={props.handleLogin}
                            handleLogout={props.handleLogout}
                            cookies={props.cookies}
                            showLogin={props.showLogin}
                            setShowLogin={props.setShowLogin}
                        />

                        <Register
                            email={email}
                            username={username}
                            password={password}
                            handleEmailChange={handleEmailChange}
                            handleUsernameChange={handleUsernameChange}
                            handlePasswordChange={handlePasswordChange}
                            cookies={props.cookies}
                        />
                    </div>
                        
                    <div className={classes.sectionMobile}>
                        <IconButton
                            aria-label="show more"
                            aria-controls={mobileMenuId}
                            aria-haspopup="true"
                            onClick={handleMobileMenuOpen}
                            color="inherit"
                        >
                            <MoreIcon />
                        </IconButton>
                    </div>
                </Toolbar>
            </AppBar>
            {renderMobileMenu}
            {renderMenu}
            {dialog}
        </div >
    );
}

function SearchResultsDialog(props) {
    const searchBarResults = props.searchBarResults;
    const history = useHistory();

    const list = searchBarResults.map((subreddit) => (
            <ListItem
                button
                onClick={(e) => (handleClick(subreddit.sr))}
                key={subreddit}
            >
                <ListItemAvatar>
                        <Avatar style={{ bgcolor: "blue" }}>
                            {subreddit.sr[0]}
                        </Avatar>
                </ListItemAvatar>
                <ListItemText primary={subreddit.sr} secondary={subreddit.title}/>
            </ListItem>
        ))

    function handleClick(sr){
        history.push("/r/" + sr)
        props.handleClose()
        window.location.reload(false);
    }

    return (
      <Dialog onClose={props.handleClose} open={props.open}>
        <DialogTitle>Matching Subreddits found:</DialogTitle>
        <List>
            {list}
        </List>
      </Dialog>
    );
  }

