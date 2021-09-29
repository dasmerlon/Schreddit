import React, { useEffect, useState, useRef  } from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Grid, Container, Hidden, CssBaseline} from "@material-ui/core";
import Post from "./Post";
import SortByBar from "./SortByBar";
import CreatePost from "./CreatePost";
import TrendingComs from "./TrendingComs";
import Premium from "./Premium";
import CommunitiesByCategory from "./PopularComs";
import Info from "./Info";
import Recommendations from "./Recommendations";
import CommentsPageBody from './comments/CommentsPageDialog';
import axios from 'axios';
import configData from './config.json'
import ErrorMessage from "./ErrorMessage";

// InfiniteScrolling source:
// https://dev.to/hunterjsbit/react-infinite-scroll-in-few-lines-588f

const useStyles = makeStyles((theme) => ({
    root: {
      backgroundColor: "#dae0e6",
    },
    grid: {
      width: '100%',
      margin: '0px',
    },
  }));

//TODO: - Sticky funktionalität vom Back-To-Top Button muss überarbeitet werden
//      - Infinit Scrolling überarbeiten
export default function ForntpageBody(props) {
    const classes = useStyles();

    const [open, setOpen] = React.useState(false);
    const [postInfo, setPostInfo] = React.useState(0);

    const [posts, setPosts] = React.useState();
    const [error, setError] = React.useState("");
    const [subredditOneLetter, setSubredditOneLetter] = React.useState("");
    const [lastSortBy, setLastSortBy] = React.useState('new');
    const [allPostsLoaded, setAllPostsLoaded] = React.useState(false);

    const [page, setPage] = useState(1);
    const loader = useRef(null);


    const handleClose = () => {
      setOpen(false);
    };

    useEffect(() => {
      getPosts(lastSortBy);
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

    const getPosts = (sortBy) => {
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

      if(typeof posts !== "undefined" && lastSortBy === sortBy){
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
              ), ((lastSortBy !== sortBy) ? true : false))
              setLastSortBy(sortBy);
        }
        else {
          setAllPostsLoaded(true);
        }
      }).catch(error => {
        setError(error)
   });
  }


    return (
    <div className={classes.root}> 
    <React.Fragment>
      <CssBaseline />
      { error !== '' &&
        <ErrorMessage error={error} setError={setError} cookies={props.cookies} setShowLogin={props.setShowLogin} handleLogout={props.handleLogout}/>
        }
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
              {props.cookies.loggedIn ? 
                <Grid item>
                  <Recommendations cookies={props.cookies}/>
                </Grid>
              : null }
              <Grid item>
                <Premium />
              </Grid>
              <Grid item>
                <TrendingComs cookies={props.cookies}/>
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
      <CommentsPageBody handleClose={handleClose} open={open} postInfo={postInfo} cookies={props.cookies}/>
    </React.Fragment>
    </div>
    );
} 


