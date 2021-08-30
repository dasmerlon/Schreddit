import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import { SvgIcon, Button, Card, CardHeader, List, ListItem, ListItemSecondaryAction, ListItemText, Link, CardContent, Typography} from "@material-ui/core"
import { mdiEmailOutline } from '@mdi/js';

const useStyles = makeStyles((theme) => ({
    card: {
        position: "sticky",
        top: "16px",
        hight: "3000px",
    },
    button: {
        position: "sticky",
        top: "870px",
        hight: "3000px",
    },
    header: {
        backgroundColor: "rgb(100, 174, 217)",
      },
  }));

// TODO: Find a better way to make the Info-Card sticky
export default function Moderators() {
    const classes = useStyles();
    
    return (
        <>
        <Card className={classes.card}>
            <CardHeader className={classes.header}
                title={
                    <Typography variant="h5" component="h2">
                        Moderators
                    </Typography>
                }
            />
            <CardContent>
                <Button startIcon={<SvgIcon ><path d={mdiEmailOutline} /></SvgIcon>} variant="outlined" color="primary">Message the mods</Button>
                <List dense>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#" >
                                    {'u/a'}
                                </Link>
                            }
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#" >
                                    {'u/b'}
                                </Link>
                            }
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#" >
                                    {'u/c'}
                                </Link>
                            }
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#" >
                                    {'u/d'}
                                </Link>
                            }
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#" >
                                    {'u/f'}
                                </Link>
                            }
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#" >
                                    {'u/g'}
                                </Link>
                            }
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#" >
                                    {'u/h'}
                                </Link>
                            }
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#" >
                                    {'u/i'}
                                </Link>
                            }
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemText/>
                        <ListItemSecondaryAction>
                            <ListItemText
                                primary={
                                    <Link href="#" >
                                        {'VIEW ALL MODERATORS'}
                                    </Link>
                                }
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                </List>
            </CardContent>
        </Card>
        
        <Button className={classes.button} variant="contained" color="primary">Back to Top</Button>

        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        </>
    );
  }

  