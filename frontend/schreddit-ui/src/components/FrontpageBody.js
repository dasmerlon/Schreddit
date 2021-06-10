import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Grid, Paper, Container, Hidden, CssBaseline} from "@material-ui/core";
import Post from "./Post";
import SortByBar from "./SortByBar";
import CreatePost from "./CreatePost";
import TrendingComs from "./TrendingComs";
import CommunitiesByCategory from "./PopularComs";
import Info from "./Info";

const useStyles = makeStyles((theme) => ({
    root: {
      backgroundColor: "#dae0e6",
    },
    grid: {
      width: '100%',
      margin: '0px',
    },
    paper: {
      padding: theme.spacing(20),
      textAlign: 'center',
      color: 'rgb(255,255,255,0.8)',
      background: 'rgb(0,0,0,0.8)',
    }
  }));

//TODO: - Sticky funktionalität vom Contact Component ist hardcoded über die höhe der Seite..
//      - Back to top Button hinzufügen
export default function ForntpageBody() {
    const classes = useStyles();

    return (
    <div className={classes.root}> 
    <React.Fragment>
      <CssBaseline />

      <Container fixed >
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
                <CommunitiesByCategory />
              </Grid>
              <Grid item>
                <Paper className={classes.paper}>Top Communities (work in Progress)</Paper>
              </Grid>
              <Grid item>
                <Paper className={classes.paper}>Premium (work in Progress)</Paper>
              </Grid>
              <Grid item>
                <Info />
              </Grid>
            </Hidden>
          </Grid>
        </Grid>
      </Container>

    </React.Fragment>
    </div>
    );
} 