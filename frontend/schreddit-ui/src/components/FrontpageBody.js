import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Grid, Container, Hidden, CssBaseline} from "@material-ui/core";
import Post from "./Post";
import SortByBar from "./SortByBar";
import CreatePost from "./CreatePost";
import TrendingComs from "./TrendingComs";
import Premium from "./Premium";
import CommunitiesByCategory from "./PopularComs";
import Info from "./Info";
import TopComs from "./TopComs";

const useStyles = makeStyles((theme) => ({
    root: {
      backgroundColor: "#dae0e6",
    },
    grid: {
      width: '100%',
      margin: '0px',
    },
  }));

//TODO: - Sticky funktionalität vom Contact Component ist hardcoded über die höhe der Seite..
//      - Infinit Scrolling einbauen
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
                <TopComs />
              </Grid>
              <Grid item>
                <Premium />
              </Grid>
              <Grid item>
                <TrendingComs />
              </Grid>
              <Grid item>
                <CommunitiesByCategory />
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