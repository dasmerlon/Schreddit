import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Card, CardHeader, Avatar, SvgIcon, Link, Grid, CardActionArea, Box, Chip} from "@material-ui/core";
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import CardMedia from '@material-ui/core/CardMedia';
import im from '../a.png'; //import vom Bild

//Symbols: (Source: https://material-ui.com/components/material-icons/)
import BookmarkBorderRoundedIcon from '@material-ui/icons/BookmarkBorderRounded';
import ShareRoundedIcon from '@material-ui/icons/ShareRounded';
import MoreHorizRoundedIcon from '@material-ui/icons/MoreHorizRounded';
// Source: https://materialdesignicons.com/
import { mdiGiftOutline, mdiCommentOutline, mdiArrowUpBoldOutline, mdiArrowDownBoldOutline} from '@mdi/js';

const useStyles = makeStyles({
    root: {
      //minWidth: 300,
      //maxWidth: 650,
      display: "flex",
      
    },
    media: {
      height: 0,
      paddingTop: '50%', // 16:9 56.25%
    },
    bullet: {
      display: 'inline-block',
      margin: '0 2px',
      transform: 'scale(0.8)',
    },
    title: {
      fontSize: 14,
    },
    pos: {
      marginBottom: 12,
    },
    avatar: {
      backgroundColor: "rgb(0,180, 200)",
    },
  });

//TODO: - Subredit und Name des Nutzers in einer Zeile anzeigen.
//      - Wie sollen Mehrere Bilder/ Videos/ Paragraphe gehandhabt werden?
//      - Up- & Down-Votes einbauen. Wie soll das mit Cards gehen? Geht das überhaupt? 
//      - Für den Avatar auch ein richtiges Bild und nicht nur einen Buchstaben 
//        mit Hintergrund verwenden.
export default function Posts() {
    const classes = useStyles();
  
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

                <Grid item direction="vertical">
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

          <CardActionArea href="http://localhost:3000/">
          <CardContent>
            <Typography variant="h5" component="h2">
              How does Shutter, ISO & Apature effect your pictures? 
              <Chip label="Informative 👨‍🎓" color="secondary" href="http://localhost:3000/" clickable />
            </Typography>
          </CardContent>
          <CardMedia className={classes.media} image={im} title="b"/>
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
