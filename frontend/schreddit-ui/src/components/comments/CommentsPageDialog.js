import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Grid, IconButton, SvgIcon, Typography} from "@material-ui/core";
import Post from "../Post";
import Comment from "./Comment";

// Source: https://materialdesignicons.com/
import { mdiArrowUpBoldOutline, mdiArrowDownBoldOutline} from '@mdi/js';

const useStyles = makeStyles((theme) => ({
    root: {
        backgroundColor: "#dae0e6",   
    },
    grid: {
        width: '100%',
        margin: '0px',
        paddingTop: '8px', 
        maxWidth: "750px",
    },
    answer1: {
        paddingLeft: "20px",
    }
  }));

export default function CommentsPageBody(props) {
    const classes = useStyles();

    const commentInfos = [
        {
            indent: 0,
            commenterName:
                "UserA",
            commentText:
                "How does Shutter, ISO & Apature effect your pictures? afasdjfklöjdasfölkajsdfklöjlöHow does Shutter, ISO & Apature effect your pictures? afasdjfklöjdasfölkajsdfklöjlöHow does Shutter, ISO & Apature effect your pictures? afasdjfklöjdasfölkajsdfklöjlö", 
        },
        {
            indent: 1,
            commenterName:
                "UserB",
            commentText:
                "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        },
        {
            indent: 0,
            commenterName:
                "UserB",
            commentText:
                "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        },
        {
            indent: 1,
            commenterName:
                "UserB",
            commentText:
                "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        },
        {
            indent: 1,
            commenterName:
                "UserB",
            commentText:
                "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        },
        {
            indent: 2,
            commenterName:
                "UserB",
            commentText:
                "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        },
        {
            indent: 3,
            commenterName:
                "UserB",
            commentText:
                "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        },
        {
            indent: 1,
            commenterName:
                "UserB",
            commentText:
                "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        },
        {
            indent: 0,
            commenterName:
                "UserB",
            commentText:
                "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        },
    ];

    const comInfo = commentInfos.map((entry) =>
        <Grid item>
            <Comment commenterName={entry["commenterName"]} commentText={entry["commentText"]} commentOn={entry["indent"]}/>
        </Grid>);

    return (
        <Dialog
            open={props.open}
            onClose={props.handleClose}
            maxWidth={'lg'}
            scroll={'paper'}
            aria-labelledby="scroll-dialog-title"
            aria-describedby="scroll-dialog-description"
        >
            <DialogTitle id="scroll-dialog-title">
                        <IconButton size="small" title="More" onClick={()=>{alert('Upvote') }}> 
                            <SvgIcon ><path d={mdiArrowUpBoldOutline} /></SvgIcon>
                        </IconButton>
                        200
                        <IconButton size="small" title="More" onClick={()=>{alert('Downvote') }}> 
                            <SvgIcon ><path d={mdiArrowDownBoldOutline} /></SvgIcon>
                        </IconButton>
            </DialogTitle>
            <DialogContent >
                <DialogContentText id="scroll-dialog-description" tabIndex={-1}>
                    <Grid container spacing={3} direction='column' className={classes.grid} >
                        <Grid item>
                            <Post showVotes={false} showJoin={false}/>
                        </Grid>
                        {comInfo}
                        
                    </Grid>

                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button style={{textTransform: "none"}} onClick={props.handleClose}>Close</Button>
            </DialogActions>
        </Dialog>
    );
} 
