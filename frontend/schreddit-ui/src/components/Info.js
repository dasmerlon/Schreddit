import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import { Button, Card, List, ListItem, ListItemSecondaryAction, ListItemText, Link, CardContent, Typography} from "@material-ui/core"

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
    }
    
  }));

// TODO: Find a better way to make the Info-Card sticky
export default function Info() {
    const classes = useStyles();
 
    // This function will scroll the window to the top 
    const scrollToTop = () => {
        window.scrollTo(0, 0);
    };
 
    return (
        <>
        <Card className={classes.card}>
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
        
        <Button onClick={scrollToTop} className={classes.button} variant="contained" color="primary">Back to Top</Button>

        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        </>
    );
  }

  