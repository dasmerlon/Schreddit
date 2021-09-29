import React, { useEffect } from 'react';
import {makeStyles} from "@material-ui/core/styles";
import { IconButton, Chip, TextareaAutosize, BottomNavigation, BottomNavigationAction, FormControl, InputLabel, OutlinedInput, InputAdornment, Divider, TextField, MenuItem, SvgIcon, Grid, Container, Hidden, CssBaseline, Paper, Button, Avatar, Typography} from "@material-ui/core";
import Rules from "./Rules";
import AboutCom from "./AboutCom";
import ImageOutlinedIcon from '@material-ui/icons/ImageOutlined';
import NotesIcon from '@material-ui/icons/Notes';
import { mdiLinkVariant, mdiPlus, mdiMinus, mdiCodeBraces, mdiFormatStrikethroughVariant, mdiExponent, mdiAlertCircleOutline, mdiFormatSize } from '@mdi/js';
import FormatBoldIcon from '@material-ui/icons/FormatBold';
import FormatItalicIcon from '@material-ui/icons/FormatItalic';
import ListIcon from '@material-ui/icons/List';
import FormatListNumberedIcon from '@material-ui/icons/FormatListNumbered';
import FormatQuoteIcon from '@material-ui/icons/FormatQuote';
import axios from 'axios';
import configData from './config.json'
import { useHistory } from "react-router-dom"
import ErrorMessage from "./ErrorMessage";

//TODO: - Code aufräumen
//      - Textfeldgröße an Fenstergröße anpassen
//      - Reddit Rules Sidepanel erstellen
//      - Router für diesen Link anpassen

const useStyles = makeStyles((theme) => ({
    root: {
      backgroundColor: "#dae0e6",
    },
    grid: {
      width: '100%',
      margin: '0px',
    },
    avatarSizeSmall: {
      width: theme.spacing(3),
      height: theme.spacing(3),
    },
    dropDown: {
      backgroundColor: "white"
    },
    button: {
      '& > *': {
        margin: theme.spacing(-1.9),
      },
    },
    toolbar: {  
      width: '100%',
      border: `1px solid ${theme.palette.divider}`,
      borderRadius: theme.shape.borderRadius,
      backgroundColor: theme.palette.background.paper,
      color: theme.palette.text.secondary,
      '& svg': {
        margin: theme.spacing(1.5),
      },
      '& hr': {
        margin: theme.spacing(0, 0.5),
      },
    },
    upload: {
      height: 200,
    },
  }));




export default function CreatePostBody(props) {
    const classes = useStyles();
    const [navigationFocus, setnavigationFocus] = React.useState("self");
    const [spoiler, setSpoilerValue] = React.useState(false);
    const [nsfw, setNsfwValue] = React.useState(false);
    const [value, setValue] = React.useState(0);
    const [subreddit, setSubreddit] = React.useState('');
    const [titleValue, setTitleValue] = React.useState('');
    const [file, setFile] = React.useState(null);
    const [url, setUrl] = React.useState();
    const [error, setError] = React.useState('');

    const [textLink, makeTextLink] = React.useState(false);
    const [textValue, setTextFieldValue] = React.useState('');

    const [subscribedSubreddits, setSubscribedSubreddits] = React.useState([])

    let history = useHistory();

    useEffect(() => {
          getSubscribedSubreddits();
    }, [props.cookies.token]);

    const getSubscribedSubreddits = () => {
        let config = {
            headers: {'Authorization': `Bearer ${props.cookies.token}`}
        };
        axios.get(configData.USER_API_URL + '/subscriptions', config
        ).then(response => {
            setSubscribedSubreddits(response.data.subreddits);
            console.log(response.data.subreddits)
            if(response.data.subreddits.length !== 0){
              setSubreddit('r/' + response.data.subreddits[0].sr);
            }
        }).catch(error => {
            setError(error);
        });
    }

    const handleTitleChange = (event) => {
      setTitleValue(event.target.value);
    };

    const handleChange = (event) => {
      setSubreddit(event.target.value);
    };

    const handleTextfieldChange = (event) => {
      setTextFieldValue(event.target.value)
    };

    const handleUrlChange = (event) => {
      setUrl(event.target.value);
    }
    // Dies soll ein anfang sein für die verschiedenen Textmanipulationen, die in einem Texteditor möglich sind (not done yet)
    const handleBold = (event) => {
      setTextFieldValue(textValue + '**bold**');
    }
    const handleItalic = (event) => {
      setTextFieldValue(textValue + '*italics*');
    }
    const handleLinkText = (event) => {
      makeTextLink(!textLink);
      { textLink ? setTextFieldValue(textValue + '[') : setTextFieldValue(textValue + '](' +  ')')};
    }

    const handlePost = (type) => {
      console.log(titleValue)
      let parameters = {
        metadata: {
          "nsfw": nsfw,
          "spoiler": spoiler,
          sr: subreddit.substring(2,subreddit.length),
        },
        content: {
          title: titleValue
        }
      }
      if(type === "self"){
        parameters.content.text = textValue;
        parameters.metadata.type = 'self';
        createPost(parameters)
      }
      else if(type === "imageOrVideo"){
        var formData = new FormData();
        formData.append("file", file)
        axios.post(configData.UPLOAD_API_URL, formData, {
          headers: {
            'Authorization': `Bearer ${props.cookies.token}`,
            'Content-Type': 'multipart/form-data'
          }
        }).then(response => {
          parameters.content.url = response.data
          if(file.type.startsWith('image')){
            parameters.metadata.type = 'image';
          }
          else if(file.type.startsWith('video')){
            parameters.metadata.type = "video";
          }
          createPost(parameters)
        }).catch(error => {
            setError(error)
        })
      }
      else if (type === "link"){
        parameters.content.url = url;
        parameters.metadata.type = 'link';
        createPost(parameters);
      } 
    }
    const createPost = (parameters) => {
      
      axios.post(configData.POST_API_URL, parameters, {
        headers: {'Authorization': `Bearer ${props.cookies.token}`}
      }).then(response => {
        history.push('/' + subreddit)
      }).catch(error => {
          setError(error)
      })
    }



    return (
    <div className={classes.root}>
        { error !== '' &&
        <ErrorMessage error={error} setError={setError} cookies={props.cookies} setShowLogin={props.setShowLogin} handleLogout={props.handleLogout}/>
        }
        <React.Fragment>
          <CssBaseline />
          <Container fixed >
            <Grid container spacing={2} direction='row' className={classes.grid}>
              <Grid item container spacing={3} direction='column' className={classes.grid} xs={12} md={7}>
                <Grid item>
                  <Grid container direction='row' justify="space-between" className={classes.grid}>
                    <Grid item >
                      <Typography variant="h5"> Create a post</Typography>
                    </Grid>
                  </Grid>
                  <Divider/>
                  <Grid container spacing={2} direction="column" className={classes.grid}>
                    <Grid item>
                      <TextField className={classes.dropDown} id="outlined-select-currency" select value={subreddit} onChange={handleChange} variant="outlined"> */}
                        {subscribedSubreddits.map((option, i) => (
                          <MenuItem key={i} value={"r/" + option.sr}>
                            <Grid container direction="row" spacing={1}>
                              <Grid item>
                                <Avatar className={classes.avatarSizeSmall}>{option.sr[0]}</Avatar>
                              </Grid>
                              <Grid item>
                                {"r/" + option.sr}
                              </Grid>
                            </Grid>
                          </MenuItem>
                        ))}
                       </TextField>
                    </Grid>
                    <Grid item>
                        <Paper>
                          <BottomNavigation value={value} onChange={(event, newValue) => {setValue(newValue);}} showLabels >
                            <BottomNavigationAction label="Post" icon={<NotesIcon />} onClick={() => setnavigationFocus("self")} />
                            <Divider orientation="vertical"/>
                            <BottomNavigationAction label="Image & Video" icon={<ImageOutlinedIcon />} onClick={() => setnavigationFocus("imageOrVideo")} />
                            <Divider orientation="vertical"/>
                            <BottomNavigationAction label="Link" icon={<SvgIcon ><path d={mdiLinkVariant} /></SvgIcon>} onClick={() => setnavigationFocus("link")} />
                          </BottomNavigation>
                          <Divider />
                          <Grid container spacing={2} direction='column' className={classes.grid}>
                            <Grid item>
                              <FormControl fullWidth variant="outlined">
                                <InputLabel htmlFor="outlined-adornment-password">Title</InputLabel>
                                <OutlinedInput
                                  id="outlined-adornment-password"
                                  type={'text' }
                                  onChange={handleTitleChange}
                                  endAdornment={<InputAdornment position="end">{titleValue.length}/300</InputAdornment>}
                                  
                                  labelWidth={70}
                                />
                              </FormControl>
                            </Grid>
                              { navigationFocus=== "Post" ? 
                            <Grid item>
                              <Grid container alignItems="center" className={classes.toolbar}>
                                <IconButton className={classes.button} onClick={handleBold}>
                                  <FormatBoldIcon />
                                </IconButton>
                                <IconButton className={classes.button} onClick={handleItalic}>
                                  <FormatItalicIcon />
                                </IconButton>
                                <IconButton className={classes.button}>
                                  <SvgIcon ><path d={mdiLinkVariant} /></SvgIcon>
                                </IconButton>
                                <IconButton className={classes.button}>
                                  <SvgIcon ><path d={mdiFormatStrikethroughVariant} /></SvgIcon>
                                </IconButton>
                                <IconButton className={classes.button} onClick={console.log(textValue)}>
                                  <SvgIcon ><path d={mdiCodeBraces} /></SvgIcon>
                                </IconButton>
                                <IconButton className={classes.button}>
                                  <SvgIcon ><path d={mdiExponent} /></SvgIcon>
                                </IconButton>
                                <IconButton className={classes.button}>
                                  <SvgIcon ><path d={mdiAlertCircleOutline} /></SvgIcon>
                                </IconButton>
                                <Divider orientation="vertical"/>
                                <IconButton className={classes.button}>
                                  <SvgIcon ><path d={mdiFormatSize} /></SvgIcon>
                                </IconButton>
                                <IconButton className={classes.button}>
                                  <ListIcon />
                                </IconButton>
                                <IconButton className={classes.button}>
                                  <FormatListNumberedIcon />
                                </IconButton>
                                <IconButton className={classes.button}>
                                  <FormatQuoteIcon />
                                </IconButton>
                              </Grid>
                            </Grid>
                              : null }
                              { navigationFocus=== "self" ? 
                            <Grid item>
                              <TextareaAutosize className={classes.grid} rowsMin={10} placeholder=" Text (optional)" onChange={handleTextfieldChange}/>
                            </Grid> 
                              : navigationFocus=== "imageOrVideo" ? 
                            <Grid item>
                              <Paper variant="outlined">
                                <Grid container alignItems="center" justify="center" className={classes.upload} >
                                  <input accept="image/*,video/*" className={classes.input} id="contained-button-file" type="file" onChange={(e) => setFile(e.target.files[0])} />
                                </Grid>
                              </Paper>
                            </Grid>
                            : 
                            <Grid item>
                              <TextareaAutosize className={classes.grid} rowsMin={4} placeholder=" Url" onChange={(e) => handleUrlChange(e)} />
                            </Grid> 
                            }
                            <Grid item>
                              <Grid container spacing={1} direction='row' className={classes.grid}>
                                <Grid item>
                                  <Chip variant={spoiler ? "outlined" : "default"} onClick={() => setSpoilerValue(!spoiler)} label="SPOILER" icon={<SvgIcon ><path d={spoiler ? mdiMinus : mdiPlus} /></SvgIcon>} />
                                </Grid>
                                <Grid item>
                                  <Chip variant={nsfw ? "outlined" : "default"} onClick={() => setNsfwValue(!nsfw)} label="NSFW" icon={<SvgIcon ><path d={nsfw ? mdiMinus : mdiPlus} /></SvgIcon>} />
                                </Grid>
                              </Grid>
                            </Grid>
                            <Divider />
                            <Grid item container alignItems="flex-end">
                              <Grid item>
                                <Button onClick={() => handlePost(navigationFocus)}>Post</Button>
                                </Grid>
                            </Grid>
                          </Grid>
                        </Paper>
                      </Grid>
                    </Grid>
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
                      Reddit Rules
                    </Grid>
                  </Hidden>
                </Grid>
              </Grid>
          </Container>

        </React.Fragment>
    </div>
    );
} 