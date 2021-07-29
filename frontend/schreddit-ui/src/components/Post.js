import React from 'react';
import {makeStyles, useTheme} from "@material-ui/core/styles";
import {Card, CardHeader, Avatar, SvgIcon, Link, Grid, CardActionArea, Chip, MobileStepper} from "@material-ui/core";
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import imA from '../images/a.png'; //import vom Bild
import imB from '../images/e.jpg'; //import vom Bild
import vid from '../images/a.mp4'; //import vom Bild

//Symbols: (Source: https://material-ui.com/components/material-icons/)
import BookmarkBorderRoundedIcon from '@material-ui/icons/BookmarkBorderRounded';
import ShareRoundedIcon from '@material-ui/icons/ShareRounded';
import MoreHorizRoundedIcon from '@material-ui/icons/MoreHorizRounded';
// Source: https://materialdesignicons.com/
import { mdiGiftOutline, mdiCommentOutline, mdiArrowUpBoldOutline, mdiArrowDownBoldOutline} from '@mdi/js';

import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';

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
    img: {
      height: '50%',
      maxWidth: 700,
      overflow: 'hidden',
      display: 'block',
      width: '100%',
    },
  });

//TODO: - Wie sollen Mehrere Bilder/ Videos/ Paragraphe gehandhabt werden?
//          -> Folgendes spielt das Video ab, aber ohne Bild...
//             <CardMedia component='iframe' className={classes.media} src={vid} />
//      - Für den Avatar auch ein richtiges Bild und nicht nur einen Buchstaben 
//        mit Hintergrund verwenden.
export default function Posts() {
  const classes = useStyles();

  const show_vid = false; 
  const show_multiple_img = true;

  // Alles hier runter ist dafür Zuständig, um bei mehreren Bildern durch alle durch zu blättern:
  const theme = useTheme();
  const [activeStep, setActiveStep] = React.useState(0);
  const maxSteps = tutorialSteps.length;

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  return (
      <Card useStyles={classes.root}>
        <CardHeader
          avatar={
            <Avatar className={classes.avatar}>
              E  
            </Avatar>
          }
          action={
            <Grid container>
              <Button size="small">+Join</Button>

              <Grid item>
                <IconButton size="small" title="More" onClick={()=>{alert('Upvote') }}> 
                  <SvgIcon ><path d={mdiArrowUpBoldOutline} /></SvgIcon>
                </IconButton>
                <Typography component="h2">
                  200
                </Typography> 
                <IconButton size="small" title="More" onClick={()=>{alert('Downvote') }}> 
                  <SvgIcon ><path d={mdiArrowDownBoldOutline} /></SvgIcon>
                </IconButton>
              </Grid>
            </Grid>
          }
          title={
            <Link href="http://localhost:3000/" color="inherit">
              {'r/HowToPictures'}
            </Link>
          }
          subheader={
            <Typography component="h2">
              Posted by 
              <Link href="http://localhost:3000/" color="inherit">
                {' u/Pictureman180 '}
              </Link> 
              2 days ago
            </Typography>
          }
        />

        <CardActionArea href="http://localhost:3000/r/HowToPictures">
          <CardContent>
            <Typography variant="h5" component="h2">
              How does Shutter, ISO & Apature effect your pictures? 
              <Chip label="Informative 👨‍🎓" color="secondary" href="http://localhost:3000/" clickable />
            </Typography>
          </CardContent>

          { !show_multiple_img && !show_vid ? 
            <img alt="" className={classes.img} src={tutorialSteps[activeStep].imgPath} />
          : null }

          { show_multiple_img && !show_vid ? 
            <img alt="" className={classes.img} src={tutorialSteps[activeStep].imgPath} /> 
          : null }
        </CardActionArea>

        { show_multiple_img && !show_vid ? 
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
        
        <CardActionArea href="http://localhost:3000/r/HowToPictures">
          {show_vid && !show_multiple_img ? 
            <video className={classes.img} controls src={vid} type={'video/mp4'} id="myVideo"/> 
          : null}
        </CardActionArea>
        <CardActions>
          <Button size="small" title="Comments" startIcon={<SvgIcon ><path d={mdiCommentOutline} /></SvgIcon>} onClick={()=>{alert('Go to comments') }} >Comments</Button>
          <Button size="small" title="Give Award" startIcon={<SvgIcon ><path d={mdiGiftOutline} /></SvgIcon>} onClick={()=>{alert('Give Award') }}>Award</Button>
          <Button size="small" title="Share" startIcon={<ShareRoundedIcon />} onClick={()=>{alert('Share with') }}>Share</Button>
          <Button size="small" title="Save" startIcon={<BookmarkBorderRoundedIcon />} onClick={()=>{alert('Saved') }}>Save</Button>
          <IconButton size="small" title="More" onClick={()=>{alert('More') }}> 
            <MoreHorizRoundedIcon /> 
          </IconButton>
        </CardActions>
      </Card>
  );
} 
