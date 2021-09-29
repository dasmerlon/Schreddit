import React from 'react';
import { Avatar, Card, IconButton, makeStyles, SvgIcon, TextField} from "@material-ui/core";
import { Link } from "react-router-dom";
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
    link: {
        width: "100%",  // entspricht "fullWidth"
    }
});

export default function CreatePost(props) {
    const classes = useStyles();

    return (
        <Card>
            <CardActions>
                <Avatar className={classes.avatar}>
                    {((typeof props !== "undefined" && typeof props.cookies !== "undefined" && typeof props.cookies.username !== "undefined" ) ? props.cookies.username[0] : "")}
                </Avatar>
                <Link className={classes.link} to={{ pathname:'/submit', state: [{id: 1, name: 'Ford', color: 'red'}] }}>
                    <TextField id="outlined-basic" label="Create Post" variant="outlined" fullWidth className={classes.textField} />
                </Link>
                <IconButton size="small" title="More" href="/submit">
                    <SvgIcon ><path d={mdiImageMultipleOutline} /></SvgIcon>
                </IconButton>
                <IconButton size="small" title="More" href="/submit">
                    <SvgIcon ><path d={mdiLinkVariant} /></SvgIcon>
                </IconButton>
            </CardActions>
        </Card>
    );
} 
