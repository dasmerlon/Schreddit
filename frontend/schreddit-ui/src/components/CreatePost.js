import React from 'react';
import {Avatar, Card, IconButton, makeStyles, SvgIcon, TextField} from "@material-ui/core";
import CardActions from '@material-ui/core/CardActions';
//Symbols: (Source: https://materialdesignicons.com/)
import { mdiLinkVariant, mdiImageMultipleOutline } from '@mdi/js';

const useStyles = makeStyles({
    avatar: {
        backgroundColor: "rgb(0,180, 100)",
    },
    textField: {
        margin: 4,
    },
});

export default function CreatePost() {
    const classes = useStyles();
    
    return (
        <Card>
            <CardActions>
                <Avatar className={classes.avatar}>
                    P
                </Avatar>
                <TextField id="outlined-basic" label="Create Post" variant="outlined" fullWidth className={classes.textField} />
                <IconButton size="small" title="More" onClick={()=>{alert('More') }}> 
                    <SvgIcon ><path d={mdiImageMultipleOutline} /></SvgIcon>
                </IconButton>
                <IconButton size="small" title="More" onClick={()=>{alert('More') }}> 
                    <SvgIcon ><path d={mdiLinkVariant} /></SvgIcon>
                </IconButton>
            </CardActions>
        </Card>
    );
} 
