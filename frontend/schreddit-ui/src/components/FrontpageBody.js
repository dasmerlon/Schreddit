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
import TopComs from "./TopComs";

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

    const [postList, setPostList] = useState({
      list: [<Post/>,<Post/>,<Post/>,<Post/>]
    }); 
    const [page, setPage] = useState(1);
    const loader = useRef(null);

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

    useEffect(() => {
      // here we simulate adding new posts to List
      const newList = postList.list.concat([<Post/>, <Post/>, <Post/>, <Post/>]);
      setPostList({
        list: newList
      })
    }, [page]);

    // here we handle what happens when user scrolls to Load More div
    // in this case we just update page variable
    const handleObserver = (entities) => {
      const target = entities[0];
      if (target.isIntersecting) {   
        setPage((page) => page + 1)
      }
    };

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
              {
                postList.list.map((post, index) => {
                  return (<div key={index} className="post" >
                    <h2> {post } </h2>
                  </div>)
                })
              }
              <div className="loading" ref={loader}>
                <h2>Loading Posts ...</h2>
              </div>
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