import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Card, List, ListItem, ListItemSecondaryAction, ListItemText, ListSubheader, Link, CardContent, Typography} from "@material-ui/core"

const useStyles = makeStyles((theme) => ({
    root: {
        position: "sticky",
        top: "1rem",
        hight: "3000px",
    }
    
  }));

// TODO: Find a better way to make the Info-Card sticky
export default function Info() {
    const classes = useStyles();
    
    return (
        <>
        <Card className={classes.root}>
            <CardContent>
                <List dense>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#"  color="inherit">
                                    {'Help'}
                                </Link>
                            }
                        />
                        <ListItemSecondaryAction>
                            <ListItemText
                                primary={
                                    <Link href="#"  color="inherit">
                                        {'About'}
                                    </Link>
                                }
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#"  color="inherit">
                                    {'Reddit App'}
                                </Link>
                            }
                        />
                        <ListItemSecondaryAction>
                            <ListItemText
                                primary={
                                    <Link href="#"  color="inherit">
                                        {'Careers'}
                                    </Link>
                                }
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#"  color="inherit">
                                    {'Reddit Coins'}
                                </Link>
                            }
                        />
                        <ListItemSecondaryAction>
                            <ListItemText
                                primary={
                                    <Link href="#"  color="inherit">
                                        {'Press'}
                                    </Link>
                                }
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#"  color="inherit">
                                    {'Reddit Premium'}
                                </Link>
                            }
                        />
                        <ListItemSecondaryAction>
                            <ListItemText
                                primary={
                                    <Link href="#"  color="inherit">
                                        {'Advertise'}
                                    </Link>
                                }
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#"  color="inherit">
                                    {'Reddit Gifts'}
                                </Link>
                            }
                        />
                        <ListItemSecondaryAction>
                            <ListItemText
                                primary={
                                    <Link href="#"  color="inherit">
                                        {'Blog'}
                                    </Link>
                                }
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#"  color="inherit">
                                    {'Communities'}
                                </Link>
                            }
                        />
                        <ListItemSecondaryAction>
                            <ListItemText
                                primary={
                                    <Link href="#"  color="inherit">
                                        {'Terms'}
                                    </Link>
                                }
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#"  color="inherit">
                                    {'Rereddit'}
                                </Link>
                            }
                        />
                        <ListItemSecondaryAction>
                            <ListItemText
                                primary={
                                    <Link href="#"  color="inherit">
                                        {'Content Policy'}
                                    </Link>
                                }
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                    <ListItem>
                        <ListItemText
                            primary={
                                <Link href="#"  color="inherit">
                                    {'Topics'}
                                </Link>
                            }
                        />
                        <ListItemSecondaryAction>
                            <ListItemText
                                primary={
                                    <Link href="#"  color="inherit">
                                        {'Privacy Policy'}
                                    </Link>
                                }
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                    <ListItem>
                        <ListItemText/>
                        <ListItemSecondaryAction>
                            <ListItemText
                                primary={
                                    <Link href="#"  color="inherit">
                                        {'Mod Policy'}
                                    </Link>
                                }
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                </List>
                <Typography>
                    <br />
                    Reddit Inc © 2021 . All rights reserved
                </Typography>
            </CardContent>
        </Card>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        </>
    );
  }

  