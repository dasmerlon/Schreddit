import React, { useEffect } from 'react';
import {makeStyles} from "@material-ui/core/styles";
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Divider, Grid, IconButton, SvgIcon} from "@material-ui/core";
import Post from "../Post";
import Comment from "./Comment";
import CreateComment from "./CreateComment";
import configData from '../config.json';
import axios from 'axios';

// Source: https://materialdesignicons.com/
import { mdiArrowUpBoldOutline, mdiArrowDownBoldOutline} from '@mdi/js';


const useStyles = makeStyles((theme) => ({
    grid: {
        width: '100%',
        margin: '0px',
        paddingTop: '8px', 
        maxWidth: "750px",
    },
  }));

export default function CommentsPageBody(props) {
    const classes = useStyles();
    const postID = props.postInfo.uid;

    var comRequestResponse = "";
    const [comments, setComments] = React.useState("");

    useEffect(() => {
        sendGetCommentsRequest("?sort=top");
    }, [props.open]);

    function sendGetCommentsRequest(sortBy) {
        console.log(props.postInfo)
        if(props.open) {
            axios.get(configData.POST_API_URL + postID + "/tree" + sortBy)
            .then(userResponse => {
                comRequestResponse = commentMaker(userResponse.data);
                if(comRequestResponse[0] === undefined){
                    setComments("")
                } else{
                    buildComments();
                }
            })
            .catch(error => {
                console.log(error)
                comRequestResponse = ("Comments could not load... Please try again later.");
            });
        }
    }

    function buildComments(uid) {
        var g = comRequestResponse.map((entry) => {
            return entry[3] === uid ?
                <Grid item> 
                    <Comment commenterName={entry[0]} commentText={entry[1]} commentOnLevel={entry[2]} commentID={entry[3]} buildComments={buildComments}/>   
                    <CreateComment postID={uid} sendGetCommentsRequest={sendGetCommentsRequest} commentOnLevel={entry[2]} cookies={props.cookies} withSortingBar={false}/>   
                </Grid>
            :
                <Grid item>
                    <Comment commenterName={entry[0]} commentText={entry[1]} commentOnLevel={entry[2]} commentID={entry[3]} buildComments={buildComments}/>   
                </Grid>
        })
        setComments(g);
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
                        <IconButton size="small" title="More" onClick={()=>{ props.postInfo.vote(1) }}> 
                            <SvgIcon ><path d={mdiArrowUpBoldOutline} style={{ color: props.postInfo.upArrowColor }} /></SvgIcon>
                        </IconButton>
                        {props.postInfo.currentVotes}
                        <IconButton size="small" title="More" onClick={()=>{ props.postInfo.vote(-1) }}> 
                            <SvgIcon ><path d={mdiArrowDownBoldOutline} style={{ color: props.postInfo.downArrowColor }} /></SvgIcon>
                        </IconButton>
            </DialogTitle>
            <DialogContent >
                <DialogContentText id="scroll-dialog-description" tabIndex={-1}>
                    <Grid container spacing={3} direction='column' className={classes.grid} >
                        <Grid item style={{paddingLeft:20}}>
                            <Post 
                                uid={props.postInfo.uid} 
                                author={props.postInfo.author} 
                                sr={props.postInfo.sr} 
                                createdAt={props.postInfo.created_at}
                                title={props.postInfo.title}
                                type={props.postInfo.type}
                                url={props.postInfo.url}
                                text={props.postInfo.text}
                                voteCount={props.postInfo.count}
                                voteState={props.postInfo.state}
                                cookies={props.postInfo.cookies}
                                clickable={false}
                                showVotes={false}
                            />
                        </Grid>
                        <Grid item style={{paddingLeft:20}}> 
                            <CreateComment postID={postID} sendGetCommentsRequest={sendGetCommentsRequest} cookies={props.cookies} withSortingBar={true}/>   
                            <Divider style={{marginTop: 15, marginRight: 13, minWidth:700}}/>
                        </Grid>
                        {comments}
                        
                    </Grid>

                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button style={{textTransform: "none"}} onClick={props.handleClose}>Close</Button>
            </DialogActions>
        </Dialog>
    );
} 

function commentMaker(postTree) {
    var a = postTree.children;
    var count = 0;
    var temp = [];

    for (var i = 0; i < postTree.children.length; i++) {
      var b = a[i];
      whileLoop(b, temp, count);
    }

    return temp;
  }

  function forLoop(b, temp, count) {
    temp.push([b.metadata.author, b.content.text, count, b.metadata.uid]);
    count++;

    for (var j = 0; j < b.children.length; j++) {
      temp = whileLoop(b.children[j], temp, count);
    }
    return temp;
  }

  function whileLoop(b, temp, count) {
    var bLength = b.children.length;

    while (bLength > 0) {
      if (b.children.length === 1) {
        temp.push([b.metadata.author, b.content.text, count, b.metadata.uid]);

        count++;
        b = b.children[0];
        bLength = b.children.length
      } 
      else if (b.children.length > 1) {
        forLoop(b, temp, count);
        bLength = -1;
      }
    }
    if (b.children.length === 0) {
        temp.push([b.metadata.author, b.content.text, count, b.metadata.uid]);
        }
    return temp;
  }
