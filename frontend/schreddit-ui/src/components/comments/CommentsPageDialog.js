import React, { useEffect } from 'react';
import {makeStyles} from "@material-ui/core/styles";
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Divider, Grid, IconButton, SvgIcon, Typography} from "@material-ui/core";
import Post from "../Post";
import Comment from "./Comment";
import CreateComment from "./CreateComment";
import configData from '../config.json';
import axios from 'axios';

// Source: https://materialdesignicons.com/
import { mdiArrowUpBoldOutline, mdiArrowDownBoldOutline, mdiCommentMinus, mdiConsoleNetworkOutline} from '@mdi/js';


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
    const [postID, setPostID] = React.useState("4a2c8573-9d1e-49f2-8665-3fbefa32834e");

    const [comInfo, setComInfo] = React.useState("");
    const [list, setList] = React.useState("");

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

    const comInfo2 = commentInfos.map((entry) =>
        <Grid item>
            <Comment commenterName={entry["commenterName"]} commentText={entry["commentText"]} commentOn={entry["indent"]}/>
        </Grid>);


    useEffect(() => {
        sendGetCommentsRequest("?sort=top");
    }, [props.open]);

    function sendGetCommentsRequest(sortBy) {
        if(props.open) {
            axios.get(configData.POST_API_URL + postID + "/tree" + sortBy)
            .then(userResponse => {
                //console.log("list ", list)
                console.log("userResponse ", userResponse.config.url)
                setComInfo(commentMaker(userResponse.data, setList, list));
                //console.log("list", list)
            })
            .catch(error => {
                setComInfo("Comments could not load... Please try again later.");
            })
        }
    }

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
                            <Post clickable={false} showVotes={false} showJoin={false}/>
                        </Grid>
                        <Grid item> 
                                    <CreateComment postID={postID} sendGetCommentsRequest={sendGetCommentsRequest} cookies={props.cookies}/>
                                
                            <Divider style={{marginTop: 15, marginRight: 13}}/>
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

function commentMaker(postTree, setList, list) {
    setList();
    var a = postTree.children;
    //console.log("commentmaker")

    for (var i = 0; i < postTree.children.length; i++) {
      var b = a[i];
      whileLoop(b, setList, list);
      //console.log("back to mainLoop")
    }

    return 0;
  }

  function forLoop(b, setList, list) {
    //console.log("newFor", b)
    setList(list=>[list, b.content.text]);

    for (var j = 0; j < b.children.length; j++) {
      //console.log("j" + j + "; b-length" + b.children.length)
      
      //console.log("for", b)
      whileLoop(b.children[j], setList, list);
      //console.log("back from while")
    }
    return 0;
  }

  function whileLoop(b, setList, list) {
    var bLength = b.children.length;

    while (bLength > 0) {
        //console.log("while", b)
      if (b.children.length === 1) {
        setList(list=>[list, b.content.text]);
        //console.log(b.content.text)
        //console.log(list)
        b = b.children[0];
        bLength = b.children.length
      } else if (b.children.length > 1) {
        //console.log("while elif")
        forLoop(b, setList, list);
        bLength = -1
      }
    }
    if (b.children.length === 0) {
        //console.log("while 0children", b)
        setList(list=>[list, b.content.text]);
    }
    return 0;
  }
