import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Grid, Paper, Container, Hidden} from "@material-ui/core";
import Post from "./Post";
import SortByBar from "./SortByBar";
import CreatePost from "./CreatePost";
import TrendingComs from "./TrendingComs";
import Info from "./Info";

const useStyles = makeStyles((theme) => ({
    root: {
      backgroundColor: "#dae0e6",
    },
    grid: {
      width: '100%',
      margin: '0px'
    },
    paper: {
      padding: theme.spacing(20),
      textAlign: 'center',
      color: 'rgb(255,255,255,0.8)',
      background: 'rgb(0,0,0,0.8)',
    }
  }));

export default function ForntpageBody() {
    const classes = useStyles();

    return (
    <div className={classes.root} > 
      <Container >
        <Grid container spacing={2} direction='row' className={classes.grid}>
          <Grid item container spacing={3} direction='column' className={classes.grid} xs={12} md={7}>
            <Grid item>
              <CreatePost />
            </Grid>
            <Grid item>
              <SortByBar />
            </Grid>
            <Grid item>
              <Post />
            </Grid>
            <Grid item>
              <Post />
            </Grid>
            <Grid item>
            <Post />
            </Grid>
          </Grid>
          <Grid item container spacing={3} direction='column' className={classes.grid} xs={1}>
            <Hidden smDown>
              <Grid item>
                <TrendingComs />
              </Grid>
              <Grid item>
                <Info />
              </Grid>
              <Grid item>
                <Paper className={classes.paper}>Trending (work in Progress)</Paper>
              </Grid>
              <Grid item>
                <Paper className={classes.paper}>Home (work in Progress)</Paper>
              </Grid>
              <Grid item>
                <Paper className={classes.paper}>Contact (work in Progress)</Paper>
              </Grid>
            </Hidden>
          </Grid>
        </Grid>
      </Container>
    </div>
    );
} 