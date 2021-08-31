import React from 'react';
import { useEffect, useState, useRef } from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Card, CardHeader, Box, Grid, Container, Hidden, CssBaseline, Paper, CardContent, Button, Avatar, Typography} from "@material-ui/core";
import Post from "./Post";
import CreatePost from "./CreatePost";
import SortByBar from "./SortByBar";
import Rules from "./Rules";
import Moderators from "./Moderators";
import AboutCom from "./AboutCom";
import axios from 'axios';
import { useHistory } from "react-router-dom"
import configData from './config.json'


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

//TODO: - Sticky funktionalität vom Contact Component ist hardcoded über die höhe der Seite..
//      - Infinit Scrolling einbauen
export default function SubreditBody(props) {
    const classes = useStyles();

    const [posts, setPosts] = React.useState();
    const [error, setError] = React.useState("");


    const [page, setPage] = useState(1);
    const loader = useRef(null);

    useEffect(() => {
      getPosts();
    }, [page])

    useEffect(() => {
      var options = {
        root: null,
        rootMargin: "20px",
        threshold: 1.0
      };
      // initialize IntersectionObserver and attaching to Load More div
      const observer = new IntersectionObserver(handleObserver, options);
      if (loader.current) {
        observer.observe(loader.current)
      }
    }, []);

    // here we handle what happens when user scrolls to Load More div
    // in this case we just update page variable
    const handleObserver = (entities) => {
      const target = entities[0];
      if (target.isIntersecting) {   
        setPage((page) => page + 1)
      }
    };

    // Add initial posts or concatinate new to existing ones
    const handlePosts = (newPosts) => {
      if(typeof posts === "undefined"){
        setPosts(newPosts);
      }
      else{
        setPosts((posts) => posts.concat(newPosts))
      }
    }

    const getPosts = () => {
      const params = {size: 5};
      if(typeof posts !== "undefined"){
        params.after = posts[posts.length-1].props.children.props.uid
      }
      axios.get(configData.POSTS_API_URL + '/r/' + "bb617bccf8e141d3874db86b8138c0d5", { params }
      ).then(response => {
              handlePosts(response.data.data.map((post) => 
                <Grid item> 
                  <Post uid={post.metadata.uid} 
                    author={post.metadata.author} 
                    sr={post.metadata.sr} 
                    createdAt={post.metadata.created_at}
                    title={post.content.title}
                    type={post.metadata.type}
                    url={post.content.url}
                    text={post.content.text}
                    /> 
                </Grid>
              ));
          }).catch(error => {
              if (error.response.status === 422) {
                  setError({ message: "Please check your input. Something is not valid." });
              }
              else {
                  setError({ message: "Something went wrong, please try again later." });
              }
              console.log(error.response);
          })
  };

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
                  <Button variant="contained" color="inherit">Join</Button>
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
            {posts}
            <div className="loading" ref={loader}>
                <h2>Loading Posts ...</h2>
          </div>
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