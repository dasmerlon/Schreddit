import React from 'react';
import { makeStyles } from "@material-ui/core/styles";
import { Card, Divider } from "@material-ui/core";
import { CardHeader, Avatar, SvgIcon, Link } from "@material-ui/core";
import CardActions from '@material-ui/core/CardActions';
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

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

    function handleClick() {
        props.buildComments(props.commentID);
    }

    return (
        <Card fullWidth elevation={0} style={{paddingLeft: paddingLeft }}>
            <CardHeader className={classes.header}
            avatar={
                <Avatar className={classes.avatar}>
                    E  
                </Avatar>   
            }
            title={
                <Link href="http://localhost:3000/r/HowToPictures" color="inherit">
                    {props.commenterName}
                </Link>
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
                <IconButton size="small" title="More" > 
                    <SvgIcon ><path d={mdiArrowUpBoldOutline} /></SvgIcon>
                </IconButton>
                <Typography component="h2">
                    200
                </Typography> 
                <IconButton size="small" title="More"> 
                    <SvgIcon ><path d={mdiArrowDownBoldOutline} /></SvgIcon>
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