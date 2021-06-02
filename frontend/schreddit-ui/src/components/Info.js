import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Card, List, ListItem, ListItemSecondaryAction, ListItemText, ListSubheader, Link} from "@material-ui/core"

const useStyles = makeStyles((theme) => ({
    root: {
        //display: "flex",
    },
  }));

export default function Info() {
    const classes = useStyles();
    
    return (
        <Card className={classes.root}>
            <List subheader={<ListSubheader>Trending Communities</ListSubheader>} className={classes.root}>
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
            </List>
        </Card>
    );
  }

  