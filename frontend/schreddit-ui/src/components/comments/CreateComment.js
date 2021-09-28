import React, { useRef } from 'react';
import { makeStyles } from "@material-ui/core/styles";
import { Card, Grid, Typography } from "@material-ui/core";
import { TextareaAutosize } from "@material-ui/core";
import Button from '@material-ui/core/Button';
import axios from 'axios';
import configData from '../config.json';

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
    text: {
        paddingRight: "13px"
    },
  }));

export default function CreateComment(props) {
    const classes = useStyles();

    const textField = useRef(null);

    const [textValue, setTextFieldValue] = React.useState('');
    const [requestError, setRequestError] = React.useState('');
    const [sortByValue, setSortByValue] = React.useState('Top');
    const paddingLeft = props.commentOnLevel *50;

    const handleTextfieldChange = (event) => {
        setTextFieldValue(event.target.value)
    };

    const sendComment = async () => {
        console.log(props.cookies.token)
        axios.post(configData.COMMENT_API_URL + props.postID, {
            metadata: {},
            content: { text: textValue}
        },
            {
                headers: {
                    Authorization: `Bearer ${props.cookies.token}`
                }
            }).then(response => {
                setRequestError("Succesfull!")
                props.sendGetCommentsRequest("?sort=" + sortByValue.toLowerCase());
                textField.current.value = "";
                setTextFieldValue("");
            }).catch(error => {
                console.log(error)
                if (error.response.status === 422) {
                    setRequestError("Please login first befor you try to submit a comment.");
                } else {
                    setRequestError("Something went wrong, please try again later.");
                }
            })
    };

    return (
        <Card elevation={0} style={{paddingLeft: paddingLeft}} >
            <Grid container direction="column">
                <Grid item className={classes.text}>
                    <TextareaAutosize ref={textField} className={classes.grid} rowsMin={5} placeholder="Here could be your comment!" onChange={handleTextfieldChange}/>
                </Grid>
                <Grid item>
                    <Grid container justify="space-between">
                        <Grid item>
                            <Grid container spacing={1}>
                                <Grid item>
                                    <Button className={classes.button} onClick={sendComment} size="small"> Comment</Button>
                                </Grid>
                                <Grid item style={{paddingRight: 30}}>
                                    <Typography variant="caption">
                                        {requestError}
                                    </Typography>
                                </Grid>
                            </Grid>
                        </Grid>
                        { props.withSortingBar ? 
                            <Grid item>
                                <Grid container justify="space-between">
                                    <Grid item style={{marginTop: 3}}>
                                        <Typography style={{textTransform: "none"}} variant="button">
                                            Sort comments by: 
                                        </Typography>
                                    </Grid>
                                    <Grid item>
                                        <Button size="small" style={{textTransform: "none"}} onClick={(e) => (e.preventDefault(), props.sendGetCommentsRequest("?sort=top"), setSortByValue("Top"))}>Top</Button>
                                        <Button size="small" style={{textTransform: "none"}} onClick={(e) => (e.preventDefault(), props.sendGetCommentsRequest("?sort=new"), setSortByValue("New"))}>New</Button>
                                        <Button size="small" style={{textTransform: "none"}} onClick={(e) => (e.preventDefault(), props.sendGetCommentsRequest("?sort=old"), setSortByValue("Old"))}>Old</Button>
                                    </Grid>
                                </Grid>
                            </Grid> 
                        : null}
                    </Grid>
                </Grid> 
            </Grid>
        </Card>
    );
} 