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
import ErrorMessage from "./ErrorMessage";
import CommentsPageBody from './comments/CommentsPageDialog';


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

    const [open, setOpen] = React.useState(false);
    const [postInfo, setPostInfo] = React.useState(0);

    const [joinStatus, setJoinStatus] = React.useState("Join");
    const [posts, setPosts] = React.useState();
    const [error, setError] = React.useState("");
    const [subreddit, setSubreddit] = React.useState("");
    const [subredditOneLetter, setSubredditOneLetter] = React.useState("");
    const [lastSortBy, setLastSortBy] = React.useState('new');
    const [allPostsLoaded, setAllPostsLoaded] = React.useState(false);
    const [subscriberCount, setSubscriberCount] = React.useState()

    const [page, setPage] = useState(1);
    const loader = useRef(null);

    useEffect(() => {
      getSubreddit();
    }, [])

    const getSubreddit = () => {
      axios.get(configData.SUBREDDIT_API_URL + window.location.pathname.split('/')[2]
      ).then(response => {
        setSubreddit(response.data);
        setSubredditOneLetter(response.data.sr[0])
        getSubredditSubscriber();
      });
    }

    const getSubredditSubscriber = () => {
      axios.get(configData.SUBSCRIPTION_API_URL + '/' + window.location.pathname.split('/')[2] + '/subscriber'
      ).then(response => {
        setSubscriberCount(response.data)
      })
    }

    useEffect(() => {
      setPage(1);
      getSubreddit();
      getPosts(lastSortBy, true);
      setStatusForJoining(window.location.pathname.split('/')[2])
    }, [window.location.pathname])

    useEffect(() => {
      getPosts(lastSortBy, false);
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
    const handlePosts = (newPosts, clear) => {
      if(typeof posts === "undefined" || clear === true){
        setPosts(newPosts);
      }
      else{
        setPosts((posts) => posts.concat(newPosts))
      }
    }

    const getPosts = (sortBy, clear) => {
      let config = '';
      if(typeof props.cookies.token !== "undefined"){
        config = {
          headers: {'Authorization': `Bearer ${props.cookies.token}`},
          params: {
            size: 5,
            sr: window.location.pathname.split('/')[2],
            sort: sortBy
          },
        };
      }
      else {
        config = {
          params: {
            size: 5,
            sr: window.location.pathname.split('/')[2],
            sort: sortBy
          }
        }
      }

      if(typeof posts !== "undefined" && lastSortBy === sortBy && !clear){
        config.params.after = posts[posts.length-1].props.children.props.uid
      }
      axios.get(configData.POSTS_API_URL, config 
      ).then(response => {
          if(response.data.data.length !== 0){  
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
                    voteCount={post.metadata.count}
                    voteState={post.metadata.state}
                    cookies={props.cookies}
                    clickable={true}
                    setOpen={setOpen}
                    setPostInfo={setPostInfo}
                    setShowLogin={props.setShowLogin}
                    /> 
                </Grid>
              ), ((lastSortBy !== sortBy || clear) ? true : false))
              setLastSortBy(sortBy);
          } 
          else {
            setAllPostsLoaded(true);
          }
      }).catch(error => {
          setError(error)
      })
    };

    const handleClose = () => {
      setOpen(false);
    };


    function setStatusForJoining(sr) {
      if(props.cookies.loggedIn){
        axios.get(configData.SUBSCRIPTION_API_URL + '/' + sr + "/state", 
        {
          headers: {
            'Authorization': `Bearer ${props.cookies.token}`
          }
        }
      ).then(response => {
        if(response.data){
          setJoinStatus("Joined")
        } else {
          setJoinStatus("Join")          
        }
      }).catch(error => {
        setError(error);
      })
      } 
    }
    

    function handleSubscribe() {
      if(joinStatus === "Join"){
        axios.put(configData.SUBSCRIPTION_API_URL + '/' + subreddit.sr + "/sub", {},
        {
          headers: {
            'Authorization': `Bearer ${props.cookies.token}`
          }
        }
        ).then(response => {
          setStatusForJoining(subreddit.sr);
        }).catch(error => {
          setError(error);
        }) 
      } 
      else {
        axios.put(configData.SUBSCRIPTION_API_URL + '/' + subreddit.sr + "/unsub", {},
        {
          headers: {
            'Authorization': `Bearer ${props.cookies.token}`
          }
        }
        ).then(response => {
          setStatusForJoining(subreddit.sr);
        }).catch(error => {
          setError(error);
        }) 
      }

    }

    return (
    <div className={classes.root}>
    { error !== '' &&
    <ErrorMessage error={error} setError={setError} cookies={props.cookies} setShowLogin={props.setShowLogin} handleLogout={props.handleLogout}/>
    }
    <React.Fragment>
      <CssBaseline />
      <Paper variant="outlined" elevation={0} className={classes.headerBackground} />
      <Paper variant="outlined" elevation={0} className={classes.paper}>
          <CardContent className={classes.header}>
            <Container fixed>
              <Grid container alignItems="center" justify="flex-start" spacing={2}>
                <Grid item>
                  <Avatar className={classes.avatarSizeLarg}>
                    {subredditOneLetter}  
                  </Avatar>
                </Grid>

                <Grid item>
                  <Typography component="h2">
                    {subreddit.title}
                  </Typography>            
                  <Typography component="h2">
                    {'r/' + subreddit.sr}
                  </Typography>
                </Grid>
                <Grid item>
                  <Button variant="contained" color="inherit" onClick={handleSubscribe} >{joinStatus}</Button>
                </Grid>
              </Grid>
            </Container>
          </CardContent>
      </Paper>


      <Container fixed >
        <Grid container spacing={2} direction='row' className={classes.grid}>
          <Grid item container spacing={3} direction='column' className={classes.grid} xs={12} md={7}>
            <Grid item>
             <CreatePost cookies={props.cookies}/>
            </Grid>
            <Grid item>
             <SortByBar getPosts={getPosts}/>           
            </Grid>
            {posts}
            <div className="loading" ref={loader}>
                <h2>{(allPostsLoaded) ? "All posts have been loaded": "Loading Posts..."}</h2>
          </div>
          </Grid>
          <Grid item container spacing={3} direction='column' className={classes.grid} xs={1}>
            <Hidden smDown>
              <Grid item>
                <AboutCom members={subscriberCount} createdAt={subreddit.created_at} description={subreddit.description} />
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
      <CommentsPageBody handleClose={handleClose} open={open} postInfo={postInfo} cookies={props.cookies}/>
    </React.Fragment>
    </div>
    );
} 