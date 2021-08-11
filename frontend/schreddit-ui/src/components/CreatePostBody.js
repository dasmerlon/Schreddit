import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import { IconButton, Chip, TextareaAutosize, BottomNavigation, BottomNavigationAction, FormControl, InputLabel, OutlinedInput, InputAdornment, Divider, TextField, MenuItem, SvgIcon, Grid, Container, Hidden, CssBaseline, Paper, Button, Avatar, Typography} from "@material-ui/core";
import Rules from "./Rules";
import AboutCom from "./AboutCom";
import ImageOutlinedIcon from '@material-ui/icons/ImageOutlined';
import NotesIcon from '@material-ui/icons/Notes';
import { mdiLinkVariant, mdiPlus, mdiCodeBraces, mdiFormatStrikethroughVariant, mdiExponent, mdiAlertCircleOutline, mdiFormatSize } from '@mdi/js';
import FormatBoldIcon from '@material-ui/icons/FormatBold';
import FormatItalicIcon from '@material-ui/icons/FormatItalic';
import ListIcon from '@material-ui/icons/List';
import FormatListNumberedIcon from '@material-ui/icons/FormatListNumbered';
import FormatQuoteIcon from '@material-ui/icons/FormatQuote';

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


const subredits = [
    {
      value: "r/AnimalsBeingBros",
    },
    {
      value: "r/space",
    }
];

export default function CreatePostBody() {
    const classes = useStyles();
    
    const [navigationFokus, setNavigationFokus] = React.useState("Post");
    const [chipValue1, setChipValue1] = React.useState(false);
    const [chipValue2, setChipValue2] = React.useState(false);
    const [value, setValue] = React.useState(0);
    const [subredit, setSubredit] = React.useState("r/AnimalsBeingBros");
    const [titleValue, setTitleValue] = React.useState('');
    
    const [textLink, makeTextLink] = React.useState(false);
    const [textValue, setTextFieldValue] = React.useState('');


    const handleTitleChange = (event) => {
      setTitleValue(event.target.value);
    };

    const handleChange = (event) => {
      setSubredit(event.target.value);
    };

    const handleTextfieldChange = (event) => {
      { textValue.slice(-9, 0) === 'undefine' ? setTextFieldValue(' ') : setTextFieldValue(textValue + event.target.value[event.target.value.length-1])}
    };

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



    return (
    <div className={classes.root}> 
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
                    <Grid item >
                      <Button>Drafts 0</Button>
                    </Grid>
                  </Grid>
                  <Divider/>
                  <Grid container spacing={2} direction="column" className={classes.grid}>
                    <Grid item>
                      <TextField className={classes.dropDown} id="outlined-select-currency" select value={subredit} onChange={handleChange} variant="outlined">
                        {subredits.map((option) => (
                          <MenuItem value={option.value}>
                            <Grid container direction="row" spacing={1}>
                              <Grid item>
                                <Avatar className={classes.avatarSizeSmall}>{option.value[2]}</Avatar>
                              </Grid>
                              <Grid item>
                                {option.value}
                              </Grid>
                            </Grid>
                          </MenuItem>
                        ))}
                      </TextField>
                      </Grid>
                      <Grid item>
                        <Paper>
                          <BottomNavigation value={value} onChange={(event, newValue) => {setValue(newValue);}} showLabels >
                            <BottomNavigationAction label="Post" icon={<NotesIcon />} onClick={() => setNavigationFokus("Post")} />
                            <Divider orientation="vertical"/>
                            <BottomNavigationAction label="Image & Video" icon={<ImageOutlinedIcon />} onClick={() => setNavigationFokus("Image & Video")} />
                            <Divider orientation="vertical"/>
                            <BottomNavigationAction label="Link" icon={<SvgIcon ><path d={mdiLinkVariant} /></SvgIcon>} onClick={() => setNavigationFokus("Link")} />
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
                              { navigationFokus=== "Post" ? 
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
                              { navigationFokus=== "Post" ? 
                            <Grid item>
                              <TextareaAutosize className={classes.grid} rowsMin={10} placeholder=" Text (optional)" onChange={handleTextfieldChange}/>
                            </Grid> 
                              : navigationFokus==="Image & Video" ? 
                            <Grid item>
                              <Paper variant="outlined">
                                <Grid container alignItems="center" justify="center" className={classes.upload} >
                                  <input accept="image/*" className={classes.input} id="contained-button-file" multiple type="file" />
                                </Grid>
                              </Paper>
                            </Grid>
                            : 
                            <Grid item>
                              <TextareaAutosize className={classes.grid} rowsMin={4} placeholder=" Url" />
                            </Grid> 
                            }
                            <Grid item>
                              <Grid container spacing={1} direction='row' className={classes.grid}>
                                <Grid item>
                                  <Chip variant={chipValue1 ? "outlined" : "default"} onClick={() => setChipValue1(!chipValue1)} label="SPOILER" icon={<SvgIcon ><path d={mdiPlus} /></SvgIcon>} />
                                </Grid>
                                <Grid item>
                                  <Chip variant={chipValue2 ? "outlined" : "default"} onClick={() => setChipValue2(!chipValue2)} label="NSFW" icon={<SvgIcon ><path d={mdiPlus} /></SvgIcon>} />
                                </Grid>
                              </Grid>
                            </Grid>
                            <Divider />
                            <Grid item container alignItems="flex-end">
                              <Grid item>
                                <Button>Save Draft</Button>
                              </Grid>
                              <Grid item>
                                <Button>Post</Button>
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