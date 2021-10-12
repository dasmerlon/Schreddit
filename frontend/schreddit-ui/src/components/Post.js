import React, { useEffect } from 'react';
import {makeStyles, useTheme} from "@material-ui/core/styles";
import {Card, CardHeader, Avatar, SvgIcon, Link, Grid, CardActionArea, Chip, MobileStepper} from "@material-ui/core";
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import IconButton from '@material-ui/core/IconButton';
import OpenInNewIcon from '@material-ui/icons/OpenInNew'
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Tooltip from '@material-ui/core/Tooltip';
import { useHistory } from "react-router-dom"
import configData from './config.json'
import axios from 'axios';
import imA from '../images/a.png'; //import vom Bild
import imB from '../images/e.jpg'; //import vom Bild
import vid from '../images/a.mp4'; //import vom Bild

//Symbols: (Source: https://material-ui.com/components/material-icons/)
import BookmarkBorderRoundedIcon from '@material-ui/icons/BookmarkBorderRounded';
import ShareRoundedIcon from '@material-ui/icons/ShareRounded';
import MoreHorizRoundedIcon from '@material-ui/icons/MoreHorizRounded';
// Source: https://materialdesignicons.com/
import { mdiGiftOutline, mdiCommentOutline, mdiArrowUpBoldOutline, mdiArrowDownBoldOutline } from '@mdi/js';

import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';
import ErrorMessage from "./ErrorMessage";
import {DateTime} from "luxon";

const tutorialSteps = [
  {
    imgPath:
      imA,
  },
  {
    imgPath:
      imB,
  },
];

const useStyles = makeStyles({
  root: {
    display: "flex",
  },
  media: {
    height: 0,
    paddingTop: '50%', // 16:9 56.25%
  },
  avatar: {
    backgroundColor: "rgb(0,180,200)",
  },
  button: {
      textTransform:"none",
  },
  //this is okayish but could be better.
  img: {
    height: '50%',
    maxWidth: 500,
    overflow: 'hidden',
    display: 'block',
    // width: '100%',
    marginLeft: 'auto',
    marginRight: 'auto'
  },
});

//TODO: - Wie sollen Mehrere Bilder/ Videos/ Paragraphe gehandhabt werden?
//          -> Folgendes spielt das Video ab, aber ohne Bild...
//             <CardMedia component='iframe' className={classes.media} src={vid} />
//      - Für den Avatar auch ein richtiges Bild und nicht nur einen Buchstaben 
//        mit Hintergrund verwenden.
export default function Posts(props) {
  const classes = useStyles();

  const [show_vid, set_show_vid] = React.useState(false);
  const [show_multiple_img, set_show_multiple_img] = React.useState(false);
  const [show_text, set_show_text] = React.useState(false);


  let history = useHistory();

  // Alles hier runter ist dafür Zuständig, um bei mehreren Bildern durch alle durch zu blättern:
  const theme = useTheme();
  const [activeStep, setActiveStep] = React.useState(0);
  const maxSteps = tutorialSteps.length;

  const [upArrowColor, setUpArrowColor] = React.useState("");
  const [downArrowColor, setDownArrowColor] = React.useState("");
  const [newState, setNewState] = React.useState(props.voteState);
  const [currentVotes, setCurrentVotes] = React.useState(props.voteCount)
  const [error, setError] = React.useState('');

  const createdAt = DateTime.fromISO(props.createdAt)

  useEffect(() => {
    setNewState(props.voteState);
    setCurrentVotes(props.voteCount);
    handleVote(props.voteState, false);
  }, [props.uid]);
  
  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleVote = (direction, newVote) => {
    if(newVote){
        axios.get(configData.VOTE_API_URL + '/' + props.uid + '/count'
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

  const goToSubreddit = () => {
    history.push("/" + props.srName)
  }

  const vote = (direction) => {
    if (newState === 1 && direction === 1) {
      direction = 0
    }
    else if (newState === -1 && direction === -1) {
      direction = 0
    }
    axios.put(configData.VOTE_API_URL + '/' + props.uid + '/' + direction, {}, {
      headers: {
        Authorization: `Bearer ${props.cookies.token}`
      }
    }).then(response => {
      setNewState(direction);
      handleVote(direction, true);
    }).catch(error => {
      setError(error)
    })
  }

  function handleClickOpen(e) {
    e.preventDefault();
    props.setOpen(true);
    props.setPostInfo(
      {
        uid: props.uid, 
        author: props.author, 
        sr: props.sr, 
        createdAt: props.createdAt,
        title: props.title,
        type: props.type,
        url: props.url,
        text: props.text,
        voteCount: props.voteCount,
        voteState: props.voteState,
        upArrowColor: upArrowColor,
        downArrowColor: downArrowColor,
        currentVotes: currentVotes,
        handleVote: handleVote,
        vote: vote
      }
    )
  };

  return (
    <Card elevation={0} useStyles={classes.root}>
      <CardHeader
        avatar={
          <Avatar className={classes.avatar}>
          {(typeof props.author !== "undefined") ? props.author[0] : ""}     
            </Avatar>
        }
        action={
          <Grid container> 
            <Grid item>
              <IconButton size="small" title="More" onClick={() => { vote(1) }}>
                <SvgIcon ><path d={mdiArrowUpBoldOutline} style={{ color: upArrowColor }} /></SvgIcon>
              </IconButton>
              <Typography component="h2" style={{ textAlign: 'center' }}>
                {currentVotes}
              </Typography>
              <IconButton size="small" title="More" onClick={() => { vote(-1) }}>
                <SvgIcon ><path d={mdiArrowDownBoldOutline} style={{ color: downArrowColor }} /></SvgIcon>
              </IconButton>
              { error !== '' && <ErrorMessage error={error} setError={setError} cookies={props.cookies} setShowLogin={props.setShowLogin} handleLogout={props.handleLogout}/> }
            </Grid>
          </Grid>
        }
        title={
          <Link href={"/r/" + props.sr} color="inherit">
            {'r/' + props.sr}
          </Link>
        }
        subheader={
          <Typography component="h2">
            Posted by
              <Link href={"/u/" + props.author} color="inherit">
              {" u/" + props.author}
            </Link>
            <br />
            <Tooltip title={createdAt.toLocaleString(DateTime.DATETIME_FULL_WITH_SECONDS)}>
              <span>{createdAt.toRelative({locale: "en"})}</span>
            </Tooltip>
          </Typography>
        }
      />

      
      <CardActionArea onClick={props.clickable ? handleClickOpen : null}>
        <CardContent>
          <Typography variant="h5" component="h2">
            {props.title}
            {/* <Chip label="Informative 👨‍🎓" color="secondary" href="http://localhost:3000/" clickable /> */}
          </Typography>
        </CardContent>


        {props.type === "image" ?
          <img alt="" className={classes.img} src={props.url} />
          : null}

        {props.type === "link" ?
          <CardContent>
            <Link href={props.url} target="_blank">
              {props.url.replace(/^\w+:\/\//, '')} <OpenInNewIcon fontSize="inherit"/>
            </Link>
          </CardContent>
          : null}

        {props.type === "self" ?
          <CardContent>
            <Typography>{props.text.slice(0, 400)}</Typography>
          </CardContent>
          : null}
        {(props.type === "self" && show_multiple_img) || (show_text && show_vid) || (show_multiple_img && show_vid) ?
          <CardContent>
            <Typography>Internal Error... (Filetype has multiple types)</Typography>
          </CardContent>
          : null}
      </CardActionArea>

      { show_multiple_img && props.type === "image" ?
        <MobileStepper
          steps={maxSteps}
          position="static"
          variant="text"
          activeStep={activeStep}
          nextButton={
            <Button size="small" onClick={handleNext} disabled={activeStep === maxSteps - 1}>
              Next
                {theme.direction === 'rtl' ? <KeyboardArrowLeft /> : <KeyboardArrowRight />}
            </Button>
          }
          backButton={
            <Button size="small" onClick={handleBack} disabled={activeStep === 0}>
              {theme.direction === 'rtl' ? <KeyboardArrowRight /> : <KeyboardArrowLeft />}
              Back
            </Button>
          }
        />
        : null}

      <CardActionArea onClick={props.clickable ? handleClickOpen : null}>
        {(props.type === "video" || props.type === "videogif") ?
          <video className={classes.img} controls src={props.url} type={'video/mp4'} id="myVideo" />
          : null}
      </CardActionArea>
      <CardActions>
        <Button size="small" className={classes.button} title="Comments" startIcon={<SvgIcon ><path d={mdiCommentOutline} /></SvgIcon>} onClick={() => { alert('Go to comments') }} >Comments</Button>
        <Button size="small" className={classes.button} title="Give Award" startIcon={<SvgIcon ><path d={mdiGiftOutline} /></SvgIcon>} onClick={() => { alert('Give Award') }}>Award</Button>
        <Button size="small" className={classes.button} title="Share" startIcon={<ShareRoundedIcon />} onClick={() => { alert('Share with') }}>Share</Button>
        <Button size="small" className={classes.button} title="Save" startIcon={<BookmarkBorderRoundedIcon />} onClick={() => { alert('Saved') }}>Save</Button>
        <IconButton size="small" title="More" onClick={() => { alert('More') }}>
          <MoreHorizRoundedIcon />
        </IconButton>
      </CardActions>
    </Card>
  );
} 
