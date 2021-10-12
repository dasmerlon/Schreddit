import React, { useEffect } from 'react';
import { makeStyles } from "@material-ui/core/styles";
import { Card, Divider } from "@material-ui/core";
import { CardHeader, Avatar, SvgIcon, Link } from "@material-ui/core";
import CardActions from '@material-ui/core/CardActions';
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Tooltip from "@material-ui/core/Tooltip";
import axios from 'axios';
import configData from '../config.json';
import ErrorMessage from "../ErrorMessage";

// Source: https://materialdesignicons.com/
import { mdiCommentOutline, mdiArrowUpBoldOutline, mdiArrowDownBoldOutline} from '@mdi/js';
import {DateTime} from "luxon";


const useStyles = makeStyles((theme) => ({
    grid: {
        width: '100%',
        margin: '0px',
        paddingTop: '8px',
    },
    button: {
        textTransform:"none",
        padding: 0,
    },
    avatar: {
        height: "30px",
        width: "30px",
    },
    header: {
        height: "40px",
    },
    text: {
        paddingLeft: "13px"
    },
  }));

export default function Comment(props) {
    const classes = useStyles();

    const paddingLeft = props.commentOnLevel *50;

    const [upArrowColor, setUpArrowColor] = React.useState("");
    const [downArrowColor, setDownArrowColor] = React.useState("");
    const [newState, setNewState] = React.useState(props.voteState);
    const [currentVotes, setCurrentVotes] = React.useState(props.voteCount)  
    const [error, setError] = React.useState("");

    const createdAt = DateTime.fromISO(props.createdAt)

    useEffect(() => {
        setNewState(props.voteState);
        setCurrentVotes(props.voteCount);
        handleVote(props.voteState, false);
    }, [props.commentID]);

    
    const handleVote = (direction, newVote) => {
        if(newVote){
            axios.get(configData.VOTE_API_URL + '/' + props.commentID + '/count'
                ).then(response => 
                    setCurrentVotes(response.data)
            )
        }

        if (direction === 1) {
            setUpArrowColor('orange');
            setDownArrowColor('unset');
        }
        else if (direction === 0) {
            setUpArrowColor('unset');
            setDownArrowColor('unset');
        }
        else {
            setUpArrowColor('unset');
            setDownArrowColor('orange');
        }
    } 
    
    const vote = (direction) => {
        if (newState === 1 && direction === 1) {
            direction = 0
        }
        else if (newState === -1 && direction === -1) {
            direction = 0
        }
        axios.put(configData.VOTE_API_URL + '/' + props.commentID + '/' + direction, {}, {
            headers: {
                Authorization: `Bearer ${props.cookies.token}`
            }
        }).then(response => {
            setNewState(direction);
            handleVote(direction, true);
        }).catch(error => {
            setError(error);
        })
    }

    function handleClick() {
        props.buildComments(props.commentID);
    }

    return (
        <Card fullWidth elevation={0} style={{paddingLeft: paddingLeft }}>
            { error !== '' &&
                <ErrorMessage error={error} setError={setError} cookies={props.cookies} setShowLogin={props.setShowLogin} handleLogout={props.handleLogout}/>
            }
            <CardHeader className={classes.header}
            avatar={
                <Avatar className={classes.avatar} style={{backgroundColor: props.cookies.username === props.commenterName ? "#00B464" : "rgb(0,180,200)"}}>
                    {(typeof props.commenterName !== "undefined") ? props.commenterName[0] : ""}   
                </Avatar>   
            }
            title={
                <Typography variant="body2">
                    Posted by
                    <Link href={"/u/" + props.commenterName} color="inherit">
                    {" u/" + props.commenterName}
                    </Link>
                    <br />
                    <Tooltip title={createdAt.toLocaleString(DateTime.DATETIME_FULL_WITH_SECONDS)}>
                        <span>{createdAt.toRelative({locale: "en"})}</span>
                    </Tooltip>
                </Typography>
            }
            />

            <div className={classes.text}>
                <Divider orientation="vertical" />
                <div>
                    <Typography variant="subtitle1" component="h2">
                        {props.commentText}
                    </Typography>
                </div>
            </div>

            <CardActions>
                <IconButton size="small" onClick={() => { vote(1) }} > 
                    <SvgIcon ><path d={mdiArrowUpBoldOutline} style={{ color: upArrowColor }} /></SvgIcon>
                </IconButton>
                <Typography component="h2">
                    {currentVotes}
                </Typography> 
                <IconButton size="small" onClick={() => { vote(-1) }} > 
                    <SvgIcon ><path d={mdiArrowDownBoldOutline} style={{ color: downArrowColor }} /></SvgIcon>
                </IconButton>
                <Button className={classes.button} size="small" onClick={handleClick} startIcon={<SvgIcon ><path d={mdiCommentOutline} /></SvgIcon>} >Reply</Button>
                <Button className={classes.button} size="small" >Give Award</Button>
                <Button className={classes.button} size="small" >Share</Button>
                <Button className={classes.button} size="small" >Report</Button>
                <Button className={classes.button} size="small" >Save</Button>
            </CardActions>
        </Card>
    );
} 