import React from 'react';
import { makeStyles } from "@material-ui/core/styles";
import { Card, Grid, Typography } from "@material-ui/core";
import { TextareaAutosize } from "@material-ui/core";
import Button from '@material-ui/core/Button';
import axios from 'axios';
import configData from '../config.json';

// Source: https://materialdesignicons.com/
import { mdiCommentOutline, mdiArrowUpBoldOutline, mdiArrowDownBoldOutline} from '@mdi/js';

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

    const [textValue, setTextFieldValue] = React.useState('');
    const [error, setError] = React.useState('');
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
                console.log("Succesfull")
            }).catch(error => {
                if (error.response.status === 422) {
                    setError({ message: "Please login first befor to submit a comment." });
                } else {
                    setError({ message: "Something went wrong, please try again later." });
                }
            })
    };

    return (
        <Card elevation={0} style={{paddingLeft: paddingLeft}} >
            <Grid container direction="column">
                <Grid item className={classes.text}>
                    <TextareaAutosize className={classes.grid} rowsMin={5} placeholder="Here could be your comment!" onChange={handleTextfieldChange}/>
                </Grid>
                <Grid item>
                    <Grid container justify="space-between">
                        <Grid item>
                            <Button className={classes.button} onClick={sendComment} size="small"> Comment</Button>
                        </Grid>
                        <Grid item>
                            <Grid container justify="space-between">
                                <Grid item style={{marginTop: 3}}>
                                    <Typography style={{textTransform: "none"}} variant="button">
                                        Sort comments by: 
                                    </Typography>
                                </Grid>
                                <Grid item>
                                    <Button size="small" style={{textTransform: "none"}} onClick={(e) => (e.preventDefault(), props.sendGetCommentsRequest("?sort=top"))}>Top</Button>
                                    <Button size="small" style={{textTransform: "none"}} onClick={(e) => (e.preventDefault(), props.sendGetCommentsRequest("?sort=new"))}>New</Button>
                                    <Button size="small" style={{textTransform: "none"}} onClick={(e) => (e.preventDefault(), props.sendGetCommentsRequest("?sort=old"))}>Old</Button>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid> 
            </Grid>
        </Card>
    );
} 