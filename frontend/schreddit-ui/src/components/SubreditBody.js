import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Card, CardHeader, Box, Grid, Container, Hidden, CssBaseline, Paper, CardContent, Button, Avatar, Typography} from "@material-ui/core";
import Post from "./Post";
import CreatePost from "./CreatePost";
import SortByBar from "./SortByBar";
import Rules from "./Rules";
import Moderators from "./Moderators";
import AboutCom from "./AboutCom";

const useStyles = makeStyles((theme) => ({
    root: {
      backgroundColor: "#dae0e6",
    },
    grid: {
      width: '100%',
      margin: '0px',
    },
    avatarSizeLarg: {
      width: theme.spacing(7),
      height: theme.spacing(7),
    },
    headerBackground: {
      height: '100px',
      backgroundColor: 'rgb(100,174,217)'
    },
    header: {
      height: "80px",
    },
    cardHeader: {
      backgroundColor: "rgb(100, 174, 217)",
    },
    cardA: {
      maxHeight: 170,
    },
    cardB: {
      maxHeight: 150,
    }

  }));

//TODO: - Sticky funktionalität vom Back-To-Top Button muss überarbeitet werden
//      - Infinit Scrolling überarbeiten
export default function SubreditBody(props) {
    const classes = useStyles();

    return (
    <div className={classes.root}> 
    <React.Fragment>
      <CssBaseline />
      <Paper variant="outlined" elevation={0} className={classes.headerBackground} />
      <Paper variant="outlined" elevation={0} className={classes.paper}>
          <CardContent className={classes.header}>
            <Container fixed>
              <Grid container alignItems="center" justify="flex-start" spacing={2}>
                <Grid item>
                  <Avatar className={classes.avatarSizeLarg}>
                    E  
                  </Avatar>
                </Grid>

                <Grid item>
                  <Typography component="h2">
                    Catchphrase
                  </Typography>            
                  <Typography component="h2">
                    r/shortCatchphrase
                  </Typography>
                </Grid>
                <Grid item>
                  <Button variant="contained" color="inherint">Join</Button>
                </Grid>
              </Grid>
            </Container>
          </CardContent>
      </Paper>


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
                <AboutCom />
              </Grid>
              <Grid item>
                <Rules />
              </Grid>
              <Grid item>
                <Box className={classes.cardA}>
                <Card >
                  <CardHeader className={classes.cardHeader}
                    title={
                      <Typography variant="h5" component="h2">
                        Report
                      </Typography>
                    }
                  />
                  <CardContent>
                    If you see any posts that violate any of the rules, please report the post and message the mods a link to it.
                  </CardContent>
                </Card></Box>
              </Grid>
              <Grid item>
              <Card className={classes.cardB}>
                  <CardHeader className={classes.cardHeader}
                    title={
                      <Typography variant="h5" component="h2">
                        Remember
                      </Typography>
                    }
                  />
                  <CardContent>
                    Moderators reserve the right to remove content they deem harmful to the subreddit.
                  </CardContent>
                </Card>
              </Grid>
              <Grid item>
                <Moderators />
              </Grid>
            </Hidden>
          </Grid>
        </Grid>
      </Container>

    </React.Fragment>
    </div>
    );
} 