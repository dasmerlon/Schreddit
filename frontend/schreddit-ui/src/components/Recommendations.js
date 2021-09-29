import React, {useEffect} from 'react';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import Button from '@material-ui/core/Button';
import { CardContent, CardMedia, Typography, CardActionArea, Avatar, Link } from '@material-ui/core';
import ArrowUp from '@material-ui/icons/ExpandLess';
import ArrowDown from '@material-ui/icons/ExpandMore';
import img from '../images/i.jpg';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableRow from '@material-ui/core/TableRow';

import configData from './config.json';
import axios from 'axios';
import ErrorMessage from './ErrorMessage';


const useStyles = makeStyles((theme) => ({
    root: {
        //maxHeight: 10,
        //maxWidth: 345
    },
    arrowUp: {
        color: "rgb(0,220,0)",
    },
    hideArrow: {
        color: "rgb(255,255,255)",
    },
    fiCardContent: {
        color: "#ffffff",
        backgroundColor: "rgba(0,0,0,.24)"
    },
}));

// Quelle der Folgenden Exports (Fi...):
// https://codesandbox.io/s/material-ui-full-image-card-qb862?file=/src/FullImageCard/FullImageCard.js:659-792
export const FiCard = withStyles({
    root: {
      position: "relative"
    }
  })(Card);
  
export const FiCardActionArea = withStyles({
    root: {
        position: "relative"
    }
})(CardActionArea);

export const FiCardContent = withStyles({
    root: {
        position: "relative",
        backgroundColor: "transparent"
    }
})(CardContent);
  
export const FiCardMedia = withStyles({
    root: {
        position: "absolute",
        top: 0,
        right: 0,
        height: "100%",
        width: "100%"
    }
})(CardMedia);


export default function RecipeReviewCard(props) {
    const classes = useStyles();

    const [error, setError] = React.useState("");
    const [recommendations, setRecommendations] = React.useState("");

    useEffect(() => {
        axios.get(configData.USER_API_URL + "/recommendations", 
        {
            headers: {
                'Authorization': `Bearer ${props.cookies.token}`
            },
            params: {
                limit: 5
            }
        },).then(response => {
            var count = 1;
            var subreddits = response.data.subreddits
            setRecommendations(subreddits.map((subreddit) =>
                {
                    return(
                        <TableRow>
                            <TableCell style={{ width: '5px'}} component="th" scope="row">
                                {count++}.
                            </TableCell>
                            <TableCell style={{ width: '5px'}} component="th" scope="row">
                                <Avatar style={{ backgroundColor: "#ff332f"}} >
                                    {subreddit.sr[0]}
                                </Avatar>
                            </TableCell>
                            <TableCell component="th" scope="row">
                                <Link href={"/r/" + subreddit.sr} color="inherit">
                                    {'r/' + subreddit.sr}
                                </Link>
                            </TableCell>
                        </TableRow>
                    )
                }
            ));
        }).catch(error => {
            setError(error)
        });
    }, []);

    return (
        <FiCard className={classes.root}>
            { error !== '' && <ErrorMessage error={error} setError={setError} cookies={props.cookies}/> } 
            <FiCardActionArea>
                <FiCardMedia
                media="picture"
                alt="Contemplative Reptile"
                image={img}
                title="Contemplative Reptile"
                />
                <FiCardContent className={classes.fiCardContent}>
                    <Typography gutterBottom variant="h5" component="h2">
                        Recommendations
                    </Typography>
                </FiCardContent>
            </FiCardActionArea>
            <CardContent>
                <TableContainer>
                    <Table>
                        <TableBody>
                            {recommendations}
                        </TableBody>
                    </Table>
                </TableContainer>

                {/* <Button variant="contained" color="primary">
                    View All    
                </Button> */}
            </CardContent>
        </FiCard>
    );
}