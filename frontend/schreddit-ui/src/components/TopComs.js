import React from 'react';
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


export default function RecipeReviewCard() {
    const classes = useStyles();

    return (
        <FiCard className={classes.root}>
            <FiCardActionArea>
                <FiCardMedia
                media="picture"
                alt="Contemplative Reptile"
                image={img}
                title="Contemplative Reptile"
                />
                <FiCardContent className={classes.fiCardContent}>
                <Typography gutterBottom variant="h5" component="h2">
                    Top Science Communities
                </Typography>
                </FiCardContent>
            </FiCardActionArea>
            <CardContent>
                <TableContainer>
                    <Table>
                        <TableBody>
                            <TableRow>
                                <TableCell component="th" scope="row">
                                    1.
                                </TableCell>
                                <TableCell component="th" scope="row">
                                    <ArrowUp className={classes.arrowUp} />
                                </TableCell> <TableCell component="th" scope="row">
                                    <Avatar
                                        alt={`Avatar`}
                                        src={`/static/images/avatar/1.jpg`}
                                    />
                                </TableCell>
                                <TableCell component="th" scope="row">
                                    <Link href="http://localhost:3000/r/space"  color="inherit">
                                        {'r/space'}
                                    </Link>
                                </TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row">
                                    2.
                                </TableCell>
                                <TableCell component="th" scope="row">
                                    <ArrowDown color="secondary" />
                                </TableCell> <TableCell component="th" scope="row">
                                    <Avatar
                                        alt={`Avatar`}
                                        src={`/static/images/avatar/1.jpg`}
                                    />
                                </TableCell>
                                <TableCell component="th" scope="row">
                                    <Link href="http://localhost:3000/r/askscience"  color="inherit">
                                        {'r/askscience'}
                                    </Link>
                                </TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row">
                                    3.
                                </TableCell>
                                <TableCell component="th" scope="row">
                                    <ArrowDown className={classes.hideArrow} />
                                </TableCell> <TableCell component="th" scope="row">
                                    <Avatar
                                        alt={`Avatar`}
                                        src={`/static/images/avatar/1.jpg`}
                                    />
                                </TableCell>
                                <TableCell component="th" scope="row">
                                    <Link href="http://localhost:3000/r/psychology"  color="inherit">
                                        {'r/psychology'}
                                    </Link>
                                </TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row">
                                    4.
                                </TableCell>
                                <TableCell component="th" scope="row">
                                    <ArrowUp className={classes.arrowUp}/>
                                </TableCell> <TableCell component="th" scope="row">
                                    <Avatar
                                        alt={`Avatar`}
                                        src={`/static/images/avatar/1.jpg`}
                                    />
                                </TableCell>
                                <TableCell component="th" scope="row">
                                    <Link href="#"  color="inherit">
                                        {'r/chemistry'}
                                    </Link>
                                </TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell component="th" scope="row">
                                    5.
                                </TableCell>
                                <TableCell component="th" scope="row">
                                    <ArrowUp className={classes.arrowUp}/>
                                </TableCell> <TableCell component="th" scope="row">
                                    <Avatar
                                        alt={`Avatar`}
                                        src={`/static/images/avatar/1.jpg`}
                                    />
                                </TableCell>
                                <TableCell component="th" scope="row">
                                    <Link href="#"  color="inherit">
                                        {'r/physics'}
                                    </Link>
                                </TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </TableContainer>

                <Button variant="contained" color="primary">
                    View All    
                </Button>
            </CardContent>
        </FiCard>
    );
}